---
name: batch-video-maker
description: Chạy vòng lặp tự động đọc video_roadmap.md, tạo video hàng loạt theo chuẩn text-to-video-vi và đánh dấu hoàn thành. Dùng khi user yêu cầu "làm 10 video", "cày roadmap", "làm hàng loạt".
---

# 🤖 Batch Video Maker (Harness Orchestrator)

Đây là kỹ năng điều phối (Orchestrator) dành riêng cho AI Agent để tự động hóa việc sản xuất hàng loạt video từ danh sách `video_roadmap.md` mà không cần User can thiệp.

## QUY TRÌNH HOẠT ĐỘNG (LẶP LẠI CHO ĐẾN KHI ĐỦ SỐ LƯỢNG)

Đối với mỗi video cần làm, Agent phải tuần tự thực hiện các bước sau:

### BƯỚC 1: Quét và Chọn Đề Tài
- Dùng công cụ đọc file `video_roadmap.md`.
- Tìm dòng `- [ ] <Từ khóa>` đầu tiên chưa được làm.
- Tạo một biến `<slug>` tiếng Việt không dấu (VD: `computer`, `hardware`).

### BƯỚC 2: Khởi Tạo Video
- Chạy lệnh Terminal: `bash .agents/skills/text-to-video-vi/scripts/new_video.sh <slug> "<Từ khóa>"`

### BƯỚC 3: Nghiên Cứu & Chấp Bút
- Đọc luật tại `.agents/skills/text-to-video-vi/resources/style_bible.md`.
- Tạo file `videos/<slug>/source.md` trích dẫn thông tin.
- Viết `videos/<slug>/script.md` đủ 6 nhịp. **BẮT BUỘC:** Chạy lệnh `python3 .agents/skills/text-to-video-vi/scripts/syllables.py videos/<slug>/script.md` để đếm. Tổng âm tiết phải nằm trong khoảng **215 - 250**.
- Viết `videos/<slug>/scenes.js`. **Lưu ý toạ độ Y của chữ phải luôn < 1050.**

### BƯỚC 4: Kết Xuất (Build) & Tự Sửa Lỗi (Chống Đơ Máy)
- Kiểm tra tài nguyên trước khi render:
  `python3 .agents/skills/system-monitor/scripts/health_check.py --pre-flight`
- Chạy lệnh Terminal (đã tự động bật QoS utility chống đơ và điều chỉnh 1 worker):
  `bash .agents/skills/text-to-video-vi/scripts/build.sh <slug> --render --safe`
- Đọc kỹ kết quả trả về của lệnh trên:
  - 🛑 **Nếu lỗi `NoAudioReceived`:** Máy chủ giọng nói quá tải. Chạy lệnh `sleep 180` để chờ 3 phút, sau đó chạy lại lệnh build. KHÔNG ĐƯỢC BỎ CUỘC.
  - 🛑 **Nếu lỗi `icon ... does not exist`:** Mở `scenes.js` sửa tên icon và build lại.
  - 🛑 **Nếu cảnh báo `WARN ... caption band`:** Mở `scenes.js` sửa toạ độ `y` bé hơn 1050 và build lại.

### BƯỚC 5: Ghi Nhận Hoàn Thành & Nghỉ Giải Nhiệt (Cooldown)
- Khi Terminal báo `wrote videos/<slug>/out/video.mp4`, dùng công cụ sửa file `video_roadmap.md`:
  - Đổi `- [ ] <Từ khóa>` thành `- [x] <Từ khóa> (Đã hoàn thành)` để đánh dấu.
- **BẮT BUỘC NGHỈ GIẢI NHIỆT GIỮA 2 VIDEO:** Chạy lệnh giải nhiệt 15 giây để máy M1 giải phóng RAM và tản nhiệt:
  `python3 .agents/skills/system-monitor/scripts/health_check.py --cooldown 15`
- Tiếp tục quay lại **BƯỚC 1** để làm video tiếp theo.

---
**QUY TẮC THÉP CHỐNG ĐƠ / TREO MÁY (BẮT BUỘC):**
- **TUYỆT ĐỐI KHÔNG RENDER SONG SONG:** Trên máy 8GB RAM, chỉ được render tuần tự từng video một. Chạy song song nhiều video sẽ tràn RAM vào SSD Swap làm đứng toàn bộ hệ thống.
- Luôn dùng flag `--safe` khi render (`build.sh <slug> --render --safe`). Chậm hơn 20 giây mỗi video nhưng an toàn 100%.
- Nếu thấy pin yếu (<20%) hoặc máy quá nóng, hãy tạm dừng batch và báo cho người dùng.
