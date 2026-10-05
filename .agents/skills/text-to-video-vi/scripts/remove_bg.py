#!/usr/bin/env python3
"""Tách nền trắng (hoặc nền sáng đồng màu) của ảnh sản phẩm thành PNG trong suốt.

Dùng:
  python3 remove_bg.py <ảnh vào> <ảnh ra.png> [--thresh 40] [--seed X,Y ...] [--preview xem.jpg]
  python3 remove_bg.py <ảnh vào> --find-holes      # liệt kê các vùng trắng bị bao kín (gợi ý --seed)

- Tô loang từ các điểm sáng ở viền ảnh: nền nối liền với viền sẽ thành trong suốt.
- Vùng nền bị bao kín (vd. khoảng trống giữa hai quai bình gas) không chạm viền:
  chạy --find-holes để xem các vùng trắng kín (toạ độ trên ẢNH VÀO), rồi thêm
  --seed X,Y cho vùng nào là NỀN. Vùng trắng là nhãn dán/chữ thì KHÔNG seed.
- --preview: ảnh xem trước trên nền giấy kem của theme paper. LUÔN mở ra nhìn:
  vật có bị ăn mất chỗ nào trắng (nhãn dán, chữ) không, còn sót nền không.
- Ảnh ra được cắt sát vật. In kích thước để dùng trong scenes.js (IMG_W, IMG_H).
"""
import sys

import numpy as np
from PIL import Image, ImageDraw

MAGENTA = (255, 0, 255)


def find_holes(src, min_px=300):
    """Các vùng gần trắng không chạm viền ảnh, lớn hơn min_px điểm ảnh."""
    arr = np.array(Image.open(src).convert("RGB"))
    white = arr.min(axis=2) >= 225
    try:
        from scipy import ndimage
        lab, n = ndimage.label(white)
    except ImportError:
        print("Cần scipy cho --find-holes (python3 -m pip install scipy)")
        sys.exit(1)
    h, w = white.shape
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    found = []
    for i in range(1, n + 1):
        if i in edge:
            continue
        ys, xs = np.where(lab == i)
        if len(xs) < min_px:
            continue
        # điểm seed: điểm của vùng gần tâm vùng nhất
        cx, cy = xs.mean(), ys.mean()
        k = np.argmin((xs - cx) ** 2 + (ys - cy) ** 2)
        found.append((len(xs), int(xs[k]), int(ys[k]), xs.min(), ys.min(), xs.max(), ys.max()))
    found.sort(reverse=True)
    if not found:
        print("Không có vùng trắng kín nào đáng kể.")
    for size, x, y, x0, y0, x1, y1 in found[:10]:
        print(f"--seed {x},{y}   ({size} px, khung {x0},{y0}–{x1},{y1}) — kiểm tra đây là nền hay nhãn/chữ")


def main():
    a = sys.argv[1:]
    if len(a) == 2 and a[1] == "--find-holes":
        find_holes(a[0])
        return
    if len(a) < 2:
        print(__doc__)
        sys.exit(1)
    src, dst = a[0], a[1]
    thresh = int(a[a.index("--thresh") + 1]) if "--thresh" in a else 40
    seeds = [tuple(int(v) for v in a[i + 1].split(",")) for i, x in enumerate(a) if x == "--seed"]
    preview = a[a.index("--preview") + 1] if "--preview" in a else None

    im = Image.open(src).convert("RGB")
    w, h = im.size
    arr = np.array(im)
    work = im.copy()
    border = [(x, 0) for x in range(0, w, 10)] + [(x, h - 1) for x in range(0, w, 10)] \
        + [(0, y) for y in range(0, h, 10)] + [(w - 1, y) for y in range(0, h, 10)]
    for x, y in border + seeds:
        if arr[y, x].min() >= 200 and work.getpixel((x, y)) != MAGENTA:  # chỉ loang từ điểm sáng
            ImageDraw.floodfill(work, (x, y), MAGENTA, thresh=thresh)
    wa = np.array(work)
    bg = (wa[:, :, 0] == 255) & (wa[:, :, 1] == 0) & (wa[:, :, 2] == 255)
    rgba = np.dstack([arr, np.where(bg, 0, 255).astype("uint8")])
    out = Image.fromarray(rgba, "RGBA")
    bbox = out.getbbox()
    out = out.crop(bbox)
    out.save(dst)
    print(f"{dst}: {out.size[0]}x{out.size[1]} (IMG_W={out.size[0]}, IMG_H={out.size[1]}), nền bỏ {bg.mean():.0%}")
    if preview:
        pv = Image.new("RGB", out.size, (245, 238, 225))
        pv.paste(out, (0, 0), out)
        pv.save(preview)
        print(f"Xem trước: {preview}")


if __name__ == "__main__":
    main()
