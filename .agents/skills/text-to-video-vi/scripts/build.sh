#!/usr/bin/env bash
# Dựng một video trong videos/<slug>/.
#   bash .agents/skills/text-to-video-vi/scripts/build.sh <slug>            # độ dài + giọng + check + ảnh khung hình
#   bash .agents/skills/text-to-video-vi/scripts/build.sh <slug> --render   # như trên + xuất MP4 vào samples/
# Thoát với mã 2 nếu check còn ERROR/WARN (phải sửa trước khi render).
set -uo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
find_root() {  # B2V_ROOT, hoặc thư mục cha gần nhất có engine/explainroo-vi.patch, hoặc theo vị trí skill
  if [ -n "${B2V_ROOT:-}" ]; then echo "$B2V_ROOT"; return; fi
  local d="$PWD"
  while [ "$d" != "/" ]; do
    [ -f "$d/engine/explainroo-vi.patch" ] && { echo "$d"; return; }
    d="$(dirname "$d")"
  done
  (cd "$SKILL_DIR/../../.." && pwd)
}
ROOT="$(find_root)"
ENGINE="${B2V_ENGINE:-$ROOT/engine/explainroo-mac}"
SLUG="${1:?Thiếu tên video: build.sh <slug> [--render] [--safe] [--workers N]}"
RENDER=0
SAFE=0
WORKERS="${B2V_WORKERS:-}"

for arg in "$@"; do
  case "$arg" in
    --render) RENDER=1 ;;
    --safe|--eco) SAFE=1 ;;
    --workers=*) WORKERS="${arg#*=}" ;;
  esac
done

for ((i=1; i<=$#; i++)); do
  val="${!i}"
  if [ "$val" = "--workers" ]; then
    next_i=$((i+1))
    WORKERS="${!next_i:-}"
  fi
done

# Tự động tính toán số worker an toàn nếu chưa chỉ định
if [ -z "$WORKERS" ]; then
  TOTAL_MEM_BYTES=$(sysctl -n hw.memsize 2>/dev/null || echo 17179869184)
  TOTAL_MEM_GB=$((TOTAL_MEM_BYTES / 1073741824))
  if [ "$SAFE" -eq 1 ] || [ "$TOTAL_MEM_GB" -le 8 ]; then
    # Máy RAM <= 8GB hoặc bật cờ --safe: chạy 1 worker để tránh tràn RAM và đứng máy
    WORKERS=1
  elif [ "$TOTAL_MEM_GB" -le 16 ]; then
    WORKERS=2
  else
    WORKERS=4
  fi
fi

P="$ROOT/videos/$SLUG"
ER=(node "$ENGINE/bin/explainroo.js")

[ -f "$ENGINE/bin/explainroo.js" ] || { echo "Chưa cài bộ dựng. Chạy scripts/setup_mac.sh trước."; exit 1; }
for f in script.md scenes.js video.json; do
  [ -f "$P/$f" ] || { echo "Thiếu $P/$f"; exit 1; }
done

echo "== 1/4 Độ dài lời đọc"
python3 "$SKILL_DIR/scripts/syllables.py" "$P/script.md"

echo "== 2/4 Giọng đọc (NamMinh, chỉ tạo lại cảnh đã đổi)"
if ! "${ER[@]}" voice "$P"; then
  echo "LỖI tạo giọng. Nếu là NoAudioReceived/mạng: đợi 3–5 phút rồi chạy lại (câu đã có được giữ)."
  exit 1
fi

echo "== 3/4 Check bố cục, thời gian, phát âm"
OUT="$("${ER[@]}" check "$P" 2>&1)"
echo "$OUT" | tail -40
if echo "$OUT" | grep -Eq '^(ERROR|WARN) '; then
  echo "CHECK CHƯA SẠCH: sửa các dòng ERROR/WARN ở trên (scenes.js hoặc script.md) rồi chạy lại."
  exit 2
fi
echo "$OUT" | grep -q '^HINT ' && echo "(Có HINT: không bắt buộc, nhưng nên xem — thường là quãng quá lâu không có gì mới.)"

echo "== 4/4 Ảnh khung hình để XEM BẰNG MẮT"
rm -rf "$P/out/stills"
"${ER[@]}" still "$P" >/dev/null 2>&1
"${ER[@]}" sheet "$P" 2>&1 | tail -1
echo "→ Mở và nhìn: $P/out/sheet.jpg (toàn video) và $P/out/stills/<cảnh>@end.png (khung cuối từng cảnh)."
echo "  Soát: chữ đủ dấu, không đè nhau, không bị cắt, không xuống hàng xấu, khoanh/mũi tên trúng chỗ, mỗi cảnh có hình rõ."

if [ "$RENDER" -eq 1 ]; then
  TASK_PREFIX=()
  if command -v taskpolicy >/dev/null 2>&1; then
    TASK_PREFIX=(taskpolicy -c utility)
  fi
  echo "== Render MP4 (Workers: $WORKERS · QoS bảo vệ giao diện: ${TASK_PREFIX[*]:-Mặc định})"
  "${TASK_PREFIX[@]}" "${ER[@]}" render "$P" --workers "$WORKERS" || { echo "LỖI render"; exit 1; }
  mkdir -p "$ROOT/samples"
  cp "$P/out/video.mp4" "$ROOT/samples/$SLUG.mp4"
  ffmpeg -v error -y -i "$P/out/video.mp4" -c:v libx264 -crf 28 -preset veryfast \
    -c:a aac -b:a 128k -movflags +faststart "$ROOT/samples/${SLUG}_preview.mp4"
  echo "== Kiểm tra file cuối"
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$ROOT/samples/$SLUG.mp4")
  SIZE=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "$ROOT/samples/$SLUG.mp4")
  VOL=$(ffmpeg -v info -i "$ROOT/samples/$SLUG.mp4" -af volumedetect -vn -f null - 2>&1 | grep -E 'mean_volume|max_volume' | sed 's/.*] //' | tr '\n' ' ')
  echo "Thời lượng: ${DUR}s · Khổ: $SIZE · Âm lượng: $VOL"
  echo "(Đạt: khổ 1080x1920; mean_volume khoảng -14 đến -20 dB; max_volume dưới -0.5 dB.)"
  echo "File gốc (đăng TikTok): samples/$SLUG.mp4"
  echo "File nhẹ (gửi xem nhanh): samples/${SLUG}_preview.mp4"
fi
