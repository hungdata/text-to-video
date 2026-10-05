#!/usr/bin/env bash
# Tạo thư mục video mới từ mẫu.
# Dùng: bash .agents/skills/text-to-video-vi/scripts/new_video.sh <slug> "<Tiêu đề>"
#   slug: chữ thường không dấu, gạch nối, bắt đầu bằng series + số, ví dụ "ai-03-llm-la-gi", "gas-02-doi-gas"
set -euo pipefail
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
SLUG="${1:?Thiếu slug}"
TITLE="${2:?Thiếu tiêu đề}"
P="$ROOT/videos/$SLUG"
if [ -e "$P" ]; then echo "Đã có $P — chọn slug khác hoặc sửa thư mục cũ."; exit 1; fi
mkdir -p "$P/assets"
cp "$SKILL_DIR/resources/template/script.md" "$SKILL_DIR/resources/template/scenes.js" \
   "$SKILL_DIR/resources/template/video.json" "$SKILL_DIR/resources/template/source.md" "$P/"
python3 - "$P" "$TITLE" <<'EOF'
import sys, pathlib
p, title = pathlib.Path(sys.argv[1]), sys.argv[2]
for name in ("script.md", "video.json", "source.md"):
    f = p / name
    f.write_text(f.read_text(encoding="utf-8").replace("{{TITLE}}", title), encoding="utf-8")
EOF
echo "Đã tạo $P"
echo "Viết lại script.md, source.md, scenes.js (xem resources/ và examples/), rồi: bash $SKILL_DIR/scripts/build.sh $SLUG"
