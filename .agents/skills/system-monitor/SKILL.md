---
name: system-monitor
description: Theo dõi sức khỏe hệ thống (CPU, RAM, Disk, nhiệt độ) khi render video hàng loạt. Tự động phát hiện máy sắp đơ và đưa ra biện pháp giảm tải. Dùng khi cần "kiểm tra máy", "máy có lag không", "theo dõi hệ thống", hoặc tích hợp vào quy trình batch-video-maker.
---

# 🖥️ System Monitor — Chống Đơ Máy Khi Render Video

Skill này giúp Agent theo dõi sức khỏe hệ thống macOS trong quá trình tạo video hàng loạt, phát hiện sớm nguy cơ đơ máy và tự động điều chỉnh tốc độ sản xuất.

## CÁCH SỬ DỤNG

### 1. Kiểm tra nhanh 1 lần (trước khi bắt đầu render)
```bash
python3 .agents/skills/system-monitor/scripts/health_check.py
```
Kết quả trả về trạng thái:
- 🟢 **OK** → An toàn, render thoải mái.
- 🟡 **WARN** → Máy đang nóng/đầy, cần giảm tải.
- 🔴 **DANGER** → DỪNG RENDER NGAY, chờ máy hạ nhiệt.

### 2. Xuất JSON cho Agent đọc tự động
```bash
python3 .agents/skills/system-monitor/scripts/health_check.py --json
```

### 3. Theo dõi liên tục (chạy ngầm khi batch render)
```bash
python3 .agents/skills/system-monitor/scripts/health_check.py --watch 30
```
Script sẽ kiểm tra mỗi 30 giây và cảnh báo nếu hệ thống quá tải.

---

## TÍCH HỢP VÀO QUY TRÌNH LÀM VIDEO HÀNG LOẠT

Khi Agent chạy skill `batch-video-maker` để làm nhiều video liên tục, **BẮT BUỘC** phải tuân thủ quy trình sau:

### Trước mỗi video:
1. Chạy `python3 .agents/skills/system-monitor/scripts/health_check.py --json`
2. Đọc trường `status` trong kết quả JSON:
   - `"OK"` → Tiếp tục làm video bình thường.
   - `"WARN"` → Áp dụng **CHẾ ĐỘ TIẾT KIỆM**:
     - Chờ 60 giây trước khi bắt đầu video tiếp theo.
     - Render với ít worker hơn: `bash build.sh <slug> --render --workers 2`
   - `"DANGER"` → **DỪNG HOÀN TOÀN**:
     - Chờ 180 giây (3 phút) để máy hạ nhiệt.
     - Chạy `sudo purge` để giải phóng RAM cache.
     - Kiểm tra lại. Nếu vẫn DANGER → dừng batch, báo cáo cho User.

### Sau mỗi 3 video:
- Luôn chạy health check 1 lần dù trước đó OK.
- Nếu đã render liên tục 5 video, nghỉ bắt buộc 120 giây.

---

## BẢNG NGƯỠNG CẢNH BÁO

| Chỉ số        | WARN       | DANGER     | Giải thích                                |
|---------------|------------|------------|-------------------------------------------|
| CPU trung bình | ≥ 75%     | ≥ 90%     | Explainroo dùng đa luồng khi render       |
| RAM đã dùng   | ≥ 80%     | ≥ 92%     | Node.js + Chrome headless ngốn RAM        |
| Ổ cứng        | ≥ 85%     | ≥ 95%     | Mỗi video tạo ra ~50-100MB file tạm       |
| Swap           | ≥ 4GB     | —         | Swap cao = RAM thật đã hết, máy sẽ lag    |
| Nhiệt độ CPU  | ≥ 85°C    | ≥ 95°C    | MacBook tự throttle (giảm tốc) khi nóng   |

---

## CHIẾN THUẬT CHỐNG ĐƠ CHO TỪNG TÌNH HUỐNG

### Tình huống 1: CPU quá cao khi render
```
💡 Giảm worker: bash build.sh <slug> --render --workers 1
💡 Đóng Chrome, VS Code, hoặc ứng dụng nặng khác
💡 Nếu dùng MacBook, cắm sạc + kê cao máy để tản nhiệt
```

### Tình huống 2: RAM sắp hết
```
💡 Chạy: sudo purge (xóa cache RAM không cần)
💡 Đóng bớt tab trình duyệt (mỗi tab Chrome ~100-300MB)
💡 Thoát ứng dụng không dùng: Zalo, Figma, Docker...
💡 Nếu RAM < 8GB, KHÔNG nên render quá 2 video liên tục
```

### Tình huống 3: Ổ cứng gần đầy
```
💡 Xóa thư mục out/ của các video cũ đã xuất xong:
   find videos/*/out -name "*.png" -delete (chỉ xóa ảnh tạm, giữ video)
💡 Xóa file preview cũ: rm samples/*_preview.mp4
💡 Mỗi video chiếm ~50-100MB trong out/, cần ít nhất 5GB trống để batch 10 video
```

### Tình huống 4: Máy đã đơ rồi
```
🛑 Mở Activity Monitor (Command + Space, gõ Activity Monitor)
🛑 Tìm process "node" hoặc "explainroo" chiếm CPU cao nhất → Force Quit
🛑 Chờ 2 phút, chạy lại build.sh — file giọng đọc đã cache, không mất
```

---

## GHI CHÚ KỸ THUẬT

- Script không cần cài thêm thư viện (dùng 100% lệnh có sẵn trên macOS).
- Nhiệt độ CPU chỉ đọc được khi có quyền `sudo` (không bắt buộc).
- Ngưỡng cảnh báo có thể tùy chỉnh trong file `scripts/health_check.py`, phần `THRESHOLDS`.
