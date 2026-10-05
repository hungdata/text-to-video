# GĐ 0 — Nền kỹ thuật (04/10/2026)

## Đã xong
- explainroo cài và chạy trên máy ảo cloud: node, ffmpeg, Chromium đều OK (`doctor`).
  Không cần tải mô hình Kokoro/Whisper vì tiếng Việt dùng edge-tts.
- `tools/voice_vi.py`: edge-tts `vi-VN-NamMinhNeural`, `boundary="WordBoundary"`,
  xuất WAV 24 kHz + mốc từng từ, tự cắt khoảng lặng đầu/cuối và dời mốc theo.
  Tự dùng proxy (`HTTPS_PROXY`) và CA của máy ảo cloud.
  Chế độ `EXPLAINROO_VI_ENGINE=draft`: âm thanh im lặng + mốc ước lượng, để kiểm tra bố cục khi chưa có mạng.
- `src/models.js`: thêm giọng `vi-VN-NamMinhNeural`, `vi-VN-HoaiMyNeural`.
- `src/voice.js`: giọng tiếng Việt gọi `voice_vi.py`, bỏ qua Whisper.
- `src/align.js`: thêm `alignVi` (chuẩn hóa NFC, giữ dấu, ghép theo từng âm tiết; từ không ghép được thì nội suy).
- Font: thêm bộ Vietnamese cho Inter, Patrick Hand; thay Kalam (không có dấu tiếng Việt) bằng Mali trong theme `paper`.
  Lấy từ npm @fontsource (Google Fonts bị chặn). Đã kiểm tra ảnh: đủ dấu.
- `npm test` đạt. `check` không còn lỗi.
- Dự án mẫu `videos/test_vi` (hook + promise + concept, khổ TikTok, pace 1.2).

## Chưa xong
- **Chưa có giọng NamMinh thật.** Máy ảo cloud của phiên này vẫn bị chặn
  `speech.platform.bing.com` và `huggingface.co` (proxy trả 403). Cài đặt Network access mới
  chưa áp dụng cho phiên này.
- `samples/test_vi_khung.mp4` (17,5 s) chỉ là bản **xem khung hình, không có giọng**;
  thời lượng thật sẽ khoảng 20 giây khi có giọng.

## Phiên sau
1. `curl -s -o /dev/null -w '%{http_code}' https://speech.platform.bing.com/` phải khác 000.
2. Chạy `engine/setup_cloud.sh` (clone explainroo, áp `explainroo-vi.patch`, cài edge-tts, dựng `test_vi`).
3. Lưu `out/video.mp4` thành `samples/test_vi.mp4`.

## Ghi chú kỹ thuật
- Mốc `[#mark]` lấy thời điểm bắt đầu của từ ngay sau nó, nên đặt mốc **trước** cụm từ cần minh họa.
- Gợi ý `at: 'từ'` vẫn dùng `normWord` gốc (bỏ dấu, bỏ "đ"); với tiếng Việt nên dùng `[#mark]`.

## Phiên 04/10/2026 17:43
- Mạng cloud **vẫn bị chặn**: curl tới speech.platform.bing.com trả 000, proxy ghi `connect_rejected` 403 (chính sách).
  Allowlist mới chưa áp dụng cho môi trường của phiên này.
- `engine/setup_cloud.sh` chạy được tới hết bước clone, git apply, npm install, pip edge-tts; dừng ở bước `voice`
  (`SkewAdjustmentError: No server date in headers` = bị proxy chặn).
- Cầu nối thiết bị: công cụ file (list/stage/commit) dùng được; shell trên Mac (device_bash) lỗi.
- Thêm **Cách B tự động một nửa**:
  - `voice_vi.py` có engine `cache` (`EXPLAINROO_VI_ENGINE=cache`, `EXPLAINROO_VI_CACHE=<thư mục>`):
    câu nào chưa có giọng thì ghi vào `requests.json` và dùng bản draft; câu nào có `<key>.mp3 + <key>.json` thì dùng giọng thật.
  - `tools/make_voice_mac.py`: chạy trên Mac, đọc `requests.json`, tạo giọng NamMinh + mốc từng từ.
  - `videos/test_vi/voice_cache/requests.json`: 6 câu của test_vi.
- Việc tiếp: người dùng chạy trên Mac
  `pip3 install edge-tts && python3 ~/Desktop/book-to-video/tools/make_voice_mac.py ~/Desktop/book-to-video/videos/test_vi/voice_cache`
  → Claude stage voice_cache, xóa build/voice, chạy voice (engine cache) → check → render → samples/test_vi.mp4.

## Phiên 04/10/2026 17:58 — GĐ 0 XONG
- Antigravity (agent.md VIỆC 1) tạo giọng trên Mac: mạng tới Bing OK, edge-tts 7.2.8, đủ 6 câu.
- Cloud: `EXPLAINROO_VI_ENGINE=cache` → voice (3 cảnh, 100% confirmed) → check (không lỗi) → render.
- **`samples/test_vi.mp4`**: 17,0 s, 1080×1920, có giọng NamMinh; âm lượng trung bình −17,4 dB, đỉnh −1,4 dB.
- Ảnh kiểm tra: dấu tiếng Việt hiển thị đủ, phụ đề khớp giọng.
- Cần sửa ở GĐ 1: nội dung dồn nửa trên khung 9:16 (nửa dưới trống); còn chữ "explainroo.com" góc trên → thay bằng nhận diện kênh; phụ đề ngắt dòng hơi lệch ("có tên / hẳn").

## 04/10/2026 19:15 — Chuyển sang Antigravity làm toàn bộ
- Skill `.agents/skills/text-to-video-vi/` (SKILL.md + scripts/ + resources/ + examples/). Antigravity đọc tự động khi người dùng nhờ làm video.
- Bộ dựng trên Mac: `engine/explainroo-mac` (đã cài ở VIỆC 3). `engine/explainroo` cũ (gói Linux, chưa vá) không dùng nữa.
- `voice_vi.py` có tự thử lại khi máy chủ giọng trả NoAudioReceived (đã cứu câu 17/18 ở VIỆC 5). Bản vá `engine/explainroo-vi.patch` đã cập nhật.
- Tốc độ thật: ~235 âm tiết/phút cả nghỉ (225 → 57 s, 239 → 61,6 s, 197 → 48,5 s). Mục tiêu 60 s = 215–250 âm tiết.
- Video đã xong: samples/test_vi.mp4, samples/mcp-01-la-gi.mp4, samples/api-02-la-gi_antigravity.mp4 (Antigravity tự làm, điểm Claude chấm: Hook 3, Hình 3, còn lại 4–5).
- Dở dang: video gas (`videos/gas-01-binh-gas`) đã đủ giọng + sửa chữ cảnh lời hứa → agent.md VIỆC 6 (chạy thử skill, render).
- Lệnh `verify` của explainroo không dùng cho tiếng Việt (nhận dạng giọng tiếng Anh).
