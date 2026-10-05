#!/usr/bin/env bash
# Dựng lại bộ dựng tiếng Việt trên máy ảo cloud (chạy từ thư mục chứa file này).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
cd ~ && git clone --depth 1 https://github.com/vincentsch/explainroo && cd explainroo
git apply "$HERE/explainroo-vi.patch"
npm install --no-audit --no-fund
pip install --break-system-packages -q edge-tts
mkdir -p videos && cp -r "$HERE/../videos/test_vi" videos/
node bin/explainroo.js voice videos/test_vi          # giọng NamMinh thật (cần mạng tới speech.platform.bing.com)
node bin/explainroo.js check videos/test_vi
node bin/explainroo.js render videos/test_vi
