#!/usr/bin/env python3
"""Đếm âm tiết lời đọc trong script.md (cú pháp explainroo) và ước lượng thời lượng.

Dùng: python3 syllables.py videos/<slug>/script.md [--target 45|60|90]

- Bỏ dòng tiêu đề (#), dòng ghi chú (>), mốc [#ten], [pause x].
- {hiển thị|cách đọc} được đếm theo phần "cách đọc".
- Mỗi chữ cách nhau bởi khoảng trắng là một âm tiết tiếng Việt.
- Ước lượng: NamMinh pace 1.2 ≈ 235 âm tiết/phút tính cả quãng nghỉ và chuyển cảnh
  (đo trên 3 video thật 04/10/2026: 225 âm tiết → 57 s, 239 → 61,6 s, 197 → 48,5 s).
"""
import re
import sys

TARGETS = {45: (165, 185), 60: (215, 250), 90: (330, 370)}
RATE = 235.0  # âm tiết / phút, gồm nghỉ và chuyển cảnh


def spoken(line):
    line = re.sub(r"\[#[^\]]*\]", " ", line)
    line = re.sub(r"\[pause[^\]]*\]", " ", line)
    line = re.sub(r"\{([^{}|]*)\|([^{}]*)\}", r"\2", line)
    return line


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    path = args[0]
    target = 60
    if "--target" in args:
        target = int(args[args.index("--target") + 1])
    lo, hi = TARGETS.get(target, TARGETS[60])

    order, counts, scene = [], {}, None
    for raw in open(path, encoding="utf-8"):
        s = raw.strip()
        if s.startswith("## "):
            scene = s[3:].split("{")[0].strip()
            order.append(scene)
            counts[scene] = 0
            continue
        if not s or s.startswith("#") or s.startswith(">") or scene is None:
            continue
        toks = [t for t in re.split(r"\s+", spoken(s)) if re.search(r"\w", t)]
        counts[scene] += len(toks)

    total = sum(counts.values())
    for sc in order:
        n = counts[sc]
        print(f"  {sc:<12} {n:>4} âm tiết  ~{n / RATE * 60:4.1f}s")
    est = total / RATE * 60
    verdict = "ĐẠT" if lo <= total <= hi else ("NGẮN" if total < lo else "DÀI")
    print(f"  TỔNG       {total:>4} âm tiết  ~{est:4.1f}s   (mục tiêu {target}s: {lo}–{hi})  → {verdict}")


if __name__ == "__main__":
    main()
