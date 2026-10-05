#!/usr/bin/env bash
# Chuẩn bị bộ dựng video trên Mac. Chạy lại nhiều lần vẫn an toàn.
# Dùng:  bash .agents/skills/text-to-video-vi/scripts/setup_mac.sh
# In "SETUP OK" ở dòng cuối khi mọi thứ sẵn sàng.
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
PATCH="$ROOT/engine/explainroo-vi.patch"
fail() { echo "LỖI: $*"; exit 1; }

echo "Dự án: $ROOT"
echo "Bộ dựng: $ENGINE"

# 1. Công cụ hệ thống
command -v node >/dev/null || fail "chưa có Node.js (cần ≥ 20.11): brew install node"
NODE_MAJOR=$(node -p 'process.versions.node.split(".")[0]')
NODE_MINOR=$(node -p 'process.versions.node.split(".")[1]')
if [ "$NODE_MAJOR" -lt 20 ] || { [ "$NODE_MAJOR" -eq 20 ] && [ "$NODE_MINOR" -lt 11 ]; }; then
  fail "Node $(node -v) quá cũ, cần ≥ 20.11"
fi
command -v ffmpeg >/dev/null || fail "chưa có ffmpeg: brew install ffmpeg"
command -v git >/dev/null || fail "chưa có git"
command -v python3 >/dev/null || fail "chưa có python3"
echo "node $(node -v) · $(ffmpeg -version | head -1 | cut -d' ' -f1-3) · $(python3 --version)"

# 2. Thư viện Python cho giọng đọc
python3 -c "import numpy" 2>/dev/null || python3 -m pip install numpy || python3 -m pip install --user numpy || fail "không cài được numpy"
python3 -c "import edge_tts" 2>/dev/null || python3 -m pip install edge-tts || python3 -m pip install --user edge-tts || fail "không cài được edge-tts"
python3 -c "import PIL" 2>/dev/null || python3 -m pip install pillow || python3 -m pip install --user pillow || echo "cảnh báo: chưa có Pillow (chỉ cần cho remove_bg.py)"
echo "edge-tts $(python3 -c 'import edge_tts,sys; print(getattr(edge_tts,"__version__","?"))')"

# 3. Bộ dựng explainroo + bản vá tiếng Việt
if [ ! -f "$ENGINE/bin/explainroo.js" ]; then
  [ -f "$PATCH" ] || fail "thiếu $PATCH"
  echo "Cài explainroo mới vào $ENGINE"
  git clone --depth 1 https://github.com/vincentsch/explainroo "$ENGINE" || fail "git clone lỗi"
  (cd "$ENGINE" && git apply "$PATCH") || fail "git apply bản vá lỗi"
fi
[ -f "$ENGINE/src/align.js" ] && grep -q "alignVi" "$ENGINE/src/align.js" || fail "$ENGINE chưa áp bản vá tiếng Việt (xóa thư mục này rồi chạy lại script)"
if [ ! -d "$ENGINE/node_modules/playwright-core" ]; then
  (cd "$ENGINE" && npm install --no-audit --no-fund) || fail "npm install lỗi"
fi
# Bản voice_vi.py mới nhất (có tự thử lại khi máy chủ giọng từ chối)
cp "$SKILL_DIR/scripts/voice_vi.py" "$ENGINE/tools/voice_vi.py"

# 4. Kiểm tra bộ dựng (bỏ qua cảnh báo về mô hình Kokoro/Whisper: tiếng Việt không dùng)
node "$ENGINE/bin/explainroo.js" doctor 2>&1 | tail -15
echo "(2 dòng 'FAIL voice model' và 'FAIL speech check model' là BÌNH THƯỜNG: tiếng Việt dùng edge-tts, không cần các mô hình đó.)"

# 5. Mạng tới máy chủ giọng đọc
CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 https://speech.platform.bing.com/ || true)
[ "$CODE" != "000" ] || fail "không vào được speech.platform.bing.com (kiểm tra mạng/VPN)"
echo "speech.platform.bing.com: HTTP $CODE (khác 000 là được)"

# 6. Thử một câu giọng thật
TMP="$(mktemp -d)"
echo '{"text":"Xin chào, mình là giọng Nam Minh.","voice":"vi-VN-NamMinhNeural","rate":1.2,"out":"'"$TMP"'/t.wav","engine":"edge"}' \
  | python3 "$ENGINE/tools/voice_vi.py" >"$TMP/t.json" || fail "tạo giọng thử thất bại (xem lỗi ở trên)"
python3 -c "import json;d=json.load(open('$TMP/t.json'));assert d['words'],'không có mốc từ';print('giọng thử:',d['duration'],'giây,',len(d['words']),'từ')" || fail "giọng thử không hợp lệ"
rm -rf "$TMP"

echo "SETUP OK"
