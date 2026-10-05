# Hướng Dẫn Tự Động Hóa Dành Cho DeepSeek Agent (Harness)

Bạn là một AI Agent tinh nhuệ. Nhiệm vụ của bạn là sản xuất video TikTok tự động dựa trên quy trình đã có sẵn. 
Môi trường làm việc: MacOS. Framework đồ họa: Explainroo.

Hãy lặp lại vòng lặp (ReAct loop) sau đây cho đến khi đạt chỉ tiêu số lượng video do User giao:

## Bước 1: Chọn Đề Tài Từ Roadmap
- Mở và đọc file `video_roadmap.md`.
- Tìm dòng `- [ ] <Từ khóa>` đầu tiên từ trên xuống (chưa có dấu x).
- Tạo một `slug` tiếng Việt không dấu (ví dụ: `computer-la-gi`).

## Bước 2: Khởi Tạo Dự Án
- Chạy lệnh Terminal: `bash .agents/skills/text-to-video-vi/scripts/new_video.sh <slug> "<Từ khóa>"`

## Bước 3: Nghiên cứu Luật Chơi (Rất quan trọng)
- Để biết luật viết câu: Đọc `.agents/skills/text-to-video-vi/resources/style_bible.md`
- Để biết mẫu đồ họa: Đọc `.agents/skills/text-to-video-vi/examples/mcp-01-la-gi/scenes.js`

## Bước 4: Chấp Bút & Lập Trình
- Viết `videos/<slug>/source.md`: Ghi nguồn kiến thức.
- Viết `videos/<slug>/script.md`: Phân bổ 6 nhịp (hook, promise, concept, step1-3, payoff, outro). 
  **QUY TẮC THÉP:** Dùng tool kiểm tra âm tiết (`python3 .agents/skills/text-to-video-vi/scripts/syllables.py`). Tổng âm tiết BẮT BUỘC nằm trong khoảng 215 - 250 để video vừa khít 60 giây.
- Viết `videos/<slug>/scenes.js`: Code Javascript để gọi các hàm vẽ icon, chữ, hình học đồng bộ với từ khóa (Ví dụ: `at: '#từ-khóa'`). Lưu ý toạ độ trục Y của chữ phải luôn `< 1050` để không bị đè phụ đề TikTok.

## Bước 5: Kết Xuất & Chống Đơ Máy (Worker Throttling)
- **QUY TẮC SỐNG CÒN:** Máy Mac 8GB RAM BẮT BUỘC dùng 1 worker để không bị tràn RAM làm đứng máy.
- Chạy lệnh: `bash .agents/skills/text-to-video-vi/scripts/build.sh <slug> --render --safe`
- Lệnh này đã tích hợp sẵn:
  - Tự động giới hạn **1 worker** (tiết kiệm 80% RAM, chỉ tốn ~600MB thay vì 3.5GB).
  - Tự động bọc lệnh với `taskpolicy -c utility` để bảo vệ giao diện macOS, đảm bảo chuột/phím không bao giờ bị lag.
- Phân tích kỹ đầu ra (stdout/stderr):
  - Nếu gặp `edge_tts.exceptions.NoAudioReceived`: Đây là lỗi rate-limit của máy chủ Microsoft. Hãy gọi lệnh `sleep 180` (chờ 3 phút) rồi chạy lại lệnh build.
  - Nếu gặp `ERROR... icon does not exist`: Hãy sửa đổi tên icon trong file `scenes.js` rồi build lại.
  - Nếu gặp `WARN... in the caption band`: Hãy giảm giá trị Y trong `scenes.js` rồi build lại.
- Dừng sửa lỗi khi Terminal báo `no problems found` và xuất xong `samples/<slug>.mp4`.

## Bước 6: Lưu Vết & Nghỉ Giải Nhiệt (Cooldown)
- Sau khi file `.mp4` được xuất thành công, dùng công cụ sửa file `video_roadmap.md`, chuyển `- [ ]` thành `- [x] <Từ khóa> (Đã hoàn thành - slug)`.
- **BẮT BUỘC NGHỈ 15 GIÂY:** Trước khi làm video tiếp theo, chạy lệnh nghỉ: `python3 .agents/skills/system-monitor/scripts/health_check.py --cooldown 15` để chip M1 xả nhiệt và hệ điều hành thu hồi bộ nhớ.
- Tiếp tục vòng lặp mới cho từ khóa tiếp theo.
