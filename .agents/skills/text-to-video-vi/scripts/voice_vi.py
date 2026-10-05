#!/usr/bin/env python3
"""Vietnamese voice for explainroo.

Reads one JSON object on stdin:
  {"text": "...", "voice": "vi-VN-NamMinhNeural", "rate": 1.15,
   "out": "/path/chunk.wav", "engine": "edge" | "draft"}
Writes a 24 kHz mono 16-bit WAV to "out" and prints JSON on stdout:
  {"duration": s, "words": [{"text": "...", "start": s, "end": s}, ...]}

engine "edge"  : Microsoft Edge read-aloud voice through edge-tts, with word
                 boundaries from the service (no Whisper needed).
engine "draft" : no network. Silent audio with estimated word timings, only
                 for checking layout and fonts before the real voice is made.
"""
import asyncio
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import unicodedata

import numpy as np

SR = 24000
TICKS = 10_000_000  # edge-tts offsets are in 100 ns units


def nfc(s):
    return unicodedata.normalize("NFC", s)


def read_pcm(path):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
        check=True, capture_output=True,
    ).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def write_wav(path, samples):
    pcm = (np.clip(samples, -1, 1) * 32767).astype("<i2").tobytes()
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", path],
        input=pcm, check=True,
    )


def trim(samples, words, thresh=0.01, pad=0.03):
    """Cut leading/trailing silence and shift word times to match."""
    loud = np.nonzero(np.abs(samples) > thresh)[0]
    if not len(loud):
        return samples, words
    a = max(0, loud[0] - int(pad * SR))
    b = min(len(samples), loud[-1] + int(pad * SR))
    off = a / SR
    dur = (b - a) / SR
    out = []
    for w in words:
        s = min(max(0.0, w["start"] - off), dur)
        e = min(max(s, w["end"] - off), dur)
        out.append({**w, "start": round(s, 3), "end": round(e, 3)})
    return samples[a:b], out


async def edge(text, voice, rate):
    import ssl

    import edge_tts
    import edge_tts.communicate as ec

    # In Claude's cloud workspace all traffic goes through an HTTPS proxy with
    # its own CA; edge-tts ignores both unless we pass them in.
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    ca = os.environ.get("SSL_CERT_FILE") or ("/root/.ccr/ca-bundle.crt" if os.path.exists("/root/.ccr/ca-bundle.crt") else None)
    if ca:
        ec._SSL_CTX = ssl.create_default_context(cafile=ca)
    pct = round((rate - 1) * 100)
    comm = edge_tts.Communicate(text, voice, rate=f"{pct:+d}%", boundary="WordBoundary", proxy=proxy)
    audio = bytearray()
    words = []
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            audio.extend(chunk["data"])
        elif chunk["type"] == "WordBoundary":
            start = chunk["offset"] / TICKS
            words.append({"text": nfc(chunk["text"]), "start": start, "end": start + chunk["duration"] / TICKS})
    if not audio:
        raise RuntimeError("edge-tts returned no audio")
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        f.write(audio)
        mp3 = f.name
    try:
        samples = read_pcm(mp3)
    finally:
        os.unlink(mp3)
    return samples, words


def edge_retry(text, voice, rate):
    """Microsoft's read-aloud service sometimes answers with no audio
    (NoAudioReceived) or drops the connection when many requests come in a
    row. Try again a few times with growing pauses before giving up.
    EXPLAINROO_VI_RETRIES (default 4) and EXPLAINROO_VI_RETRY_SCALE (default 1)
    change how many tries and how long the pauses are."""
    tries = max(1, int(os.environ.get("EXPLAINROO_VI_RETRIES", "1")))
    scale = float(os.environ.get("EXPLAINROO_VI_RETRY_SCALE", "0.1"))
    waits = [3, 10, 30, 60]
    for k in range(tries):
        try:
            return asyncio.run(edge(text, voice, rate))
        except Exception as e:  # noqa: BLE001 - any network/service failure
            if k == tries - 1:
                print(f"voice_vi: {type(e).__name__}: {e}; fallback to draft", file=sys.stderr, flush=True)
                return draft(text, rate)
            w = waits[min(k, len(waits) - 1)] * scale
            print(f"voice_vi: {type(e).__name__}: {e}; retry in {w:.0f}s ({k + 1}/{tries})", file=sys.stderr, flush=True)
            time.sleep(w)


def draft(text, rate):
    """Silent stand-in: ~0.2 s per syllable, longer after punctuation."""
    t = 0.05
    words = []
    for tok in text.split():
        d = 0.2 / rate
        words.append({"text": tok, "start": round(t, 3), "end": round(t + d, 3)})
        t += d + (0.18 / rate if re.search(r"[,;:]$", tok) else 0.02)
    samples = np.zeros(int((t + 0.05) * SR), dtype=np.float32)
    return samples, words


def cache_key(text, voice, rate):
    import hashlib
    return hashlib.sha256(f"{voice}|{rate:.4f}|{text}".encode()).hexdigest()[:20]


def from_cache(text, voice, rate):
    """engine "cache": use voice made elsewhere (tools/make_voice_mac.py).
    Missing chunks are listed in requests.json and fall back to draft."""
    d = os.environ.get("EXPLAINROO_VI_CACHE") or os.path.join(os.getcwd(), "voice_cache")
    os.makedirs(d, exist_ok=True)
    k = cache_key(text, voice, rate)
    mp3, js = os.path.join(d, k + ".mp3"), os.path.join(d, k + ".json")
    if os.path.exists(mp3) and os.path.exists(js):
        words = [{**w, "text": nfc(w["text"])} for w in json.load(open(js, encoding="utf-8"))["words"]]
        return trim(read_pcm(mp3), words)
    rq = os.path.join(d, "requests.json")
    reqs = json.load(open(rq, encoding="utf-8")) if os.path.exists(rq) else []
    if not any(r["key"] == k for r in reqs):
        reqs.append({"key": k, "text": text, "voice": voice, "rate": rate})
        json.dump(reqs, open(rq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"voice_vi: missing cache {k}, using draft", file=sys.stderr)
    return draft(text, rate)


def main():
    req = json.load(sys.stdin)
    text = nfc(req["text"])
    rate = float(req.get("rate", 1.0))
    samples, words = draft(text, rate)
    write_wav(req["out"], samples)
    json.dump({"duration": round(len(samples) / SR, 3), "words": words}, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
