#!/usr/bin/env python3
"""Tạo giọng NamMinh trên Mac cho các câu mà máy ảo cloud cần.

Cách chạy (Terminal trên Mac):
  pip3 install edge-tts
  python3 ~/Desktop/book-to-video/tools/make_voice_mac.py ~/Desktop/book-to-video/videos/test_vi/voice_cache

Đọc <thư mục>/requests.json, ghi <key>.mp3 + <key>.json (mốc từng từ) vào cùng thư mục.
"""
import asyncio, json, os, sys

import edge_tts

TICKS = 10_000_000


async def one(r, d):
    mp3, js = os.path.join(d, r["key"] + ".mp3"), os.path.join(d, r["key"] + ".json")
    if os.path.exists(mp3) and os.path.exists(js):
        return "có sẵn"
    pct = round((r["rate"] - 1) * 100)
    comm = edge_tts.Communicate(r["text"], r["voice"], rate=f"{pct:+d}%", boundary="WordBoundary")
    audio, words = bytearray(), []
    async for c in comm.stream():
        if c["type"] == "audio":
            audio.extend(c["data"])
        elif c["type"] == "WordBoundary":
            s = c["offset"] / TICKS
            words.append({"text": c["text"], "start": s, "end": s + c["duration"] / TICKS})
    if not audio:
        raise RuntimeError("edge-tts không trả âm thanh")
    open(mp3, "wb").write(audio)
    json.dump({"words": words}, open(js, "w", encoding="utf-8"), ensure_ascii=False)
    return f"{len(words)} từ"


async def with_retry(r, d, tries=4):
    for k in range(tries):
        try:
            return await one(r, d)
        except Exception as e:  # NoAudioReceived, mạng chập chờn, bị giới hạn tốc độ
            wait = [5, 15, 30, 60][k]
            print(f"    lỗi lần {k + 1}: {type(e).__name__}; thử lại sau {wait}s")
            await asyncio.sleep(wait)
    return None


async def main(d):
    reqs = json.load(open(os.path.join(d, "requests.json"), encoding="utf-8"))
    failed = []
    for i, r in enumerate(reqs, 1):
        res = await with_retry(r, d)
        print(f"[{i}/{len(reqs)}] {r['text'][:50]}… {res or 'HỎNG'}")
        if res is None:
            failed.append(r["text"])
        elif res != "có sẵn":
            await asyncio.sleep(1.5)  # nghỉ giữa các câu để tránh bị chặn
    if failed:
        print(f"Còn {len(failed)} câu hỏng:")
        for t in failed:
            print("  -", t)
        print("Chạy lại lệnh sau vài phút (câu đã có sẽ được bỏ qua).")
        sys.exit(1)
    print("Xong. Quay lại Claude và báo 'đã tạo giọng'.")


if __name__ == "__main__":
    asyncio.run(main(os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "voice_cache")))
