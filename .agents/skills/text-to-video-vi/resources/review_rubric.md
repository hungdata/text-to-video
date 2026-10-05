# Bảng chấm video — chấm như người ngoài, không chấm như tác giả

Chấm SAU khi đã có sheet.jpg (và sau render nếu có). Mỗi điểm phải kèm **bằng chứng** (trích câu, tên cảnh, con số). Điểm không có bằng chứng = không hợp lệ.

## Luật chống tự khen

- Bắt buộc ghi **3 điểm yếu lớn nhất**, kể cả khi mọi tiêu chí ≥ 4.
- Cho 5 điểm thì phải nói được vì sao nó KHÔNG phải 4.
- Không được cho 5/5 cả 8 tiêu chí ở bản nháp đầu. (Thực tế đo được: bản đầu của mọi video đều có ít nhất 2 tiêu chí ≤ 4.)
- Độ dài lấy từ `syllables.py` và thời lượng thật của file, không ước chừng.
- So với `examples/mcp-01-la-gi` (mốc "đạt"): cảnh nào thưa hơn, chữ nào yếu hơn thì trừ điểm.

## 8 tiêu chí

| Tiêu chí | 5 | 4 | ≤ 3 (viết lại) |
|---|---|---|---|
| **Hook** | Câu hỏi/sự thật bất ngờ, dưới 12 âm tiết, gắn với đời người xem; chữ trên màn + hình động cùng nói một điều | Rõ nhưng ít bất ngờ | Câu lạ tai, mơ hồ, mở bằng tên nguồn/định nghĩa, hoặc không tạo câu hỏi trong đầu người xem |
| **Lời hứa** | Người xem biết chính xác xem xong sẽ hiểu điều gì | Hơi chung chung | Không có, hoặc hứa thứ video không trả lời |
| **Một ý** | Tóm cả video trong 1 câu, mọi cảnh phục vụ câu đó | Có 1 cảnh lạc đề nhẹ | Hai ba ý chính tranh nhau |
| **Dễ hiểu** | Học sinh lớp 9 hiểu, thuật ngữ được giải thích bằng ví dụ đời thường | Còn 1 chỗ trừu tượng | Định nghĩa sách vở, nhiều thuật ngữ |
| **Chính xác** | Mọi số liệu/khẳng định có trích NGUYÊN VĂN trong source.md và đã mở nguồn đối chiếu lại | Có chỗ diễn đạt rộng hơn nguồn một chút | Có câu không có nguồn, nói quá nguồn, hoặc bịa |
| **Hình** | Câu nào cũng có mốc; mỗi cảnh có hình chính to rõ; 2–4 s có thay đổi; không đè, không tràn | Có 1–2 cảnh thưa/nhỏ | Nhiều cảnh trống, icon bé, chữ xuống hàng xấu, đè nhau |
| **Đóng vòng** | Câu hỏi ở hook được trả lời trọn ở payoff (đọc liền thành cặp hỏi–đáp); hình mở đầu được nhắc lại | Trả lời đúng nhưng hình không quay lại | Payoff trả lời câu khác |
| **Độ dài** | Trong khoảng mục tiêu (60 s: 215–250 âm tiết, file thật 55–65 s) | Lệch ≤ 5 s | Lệch > 5 s |

## Kiểm tra máy móc (chạy trước khi chấm)

```bash
python3 .agents/skills/text-to-video-vi/scripts/syllables.py videos/<slug>/script.md
grep -n -i -E "xin chào các bạn|hãy cùng|cùng mình|follow|đăng ký kênh|thực ra|thật sự|đơn giản là|về cơ bản|bạn sẽ không tin|sốc" videos/<slug>/script.md
grep -n '"title"' videos/<slug>/video.json
```

- `grep` cụm cấm phải rỗng (trừ dòng `>`).
- Title trong video.json đúng video này.
- Mỗi con số trong lời đọc có trong source.md.

## Lỗi hay gặp ở bản nháp (đã thấy thật)

- Hook kiểu "Cắm một đoạn mã, website có ngay bản đồ": ý đúng nhưng câu lạ tai, không có câu hỏi → viết lại thành câu hỏi người thường từng tự hỏi.
- Định nghĩa trừu tượng ("giao diện giúp phần mềm kết nối") → thay bằng việc nó làm cho người dùng, kèm ví dụ.
- Cảnh chỉ có 2–3 icon 70 px giữa nền trống → thêm hình chính 150–200 px hoặc sơ đồ.
- Ghi "~234 âm tiết" trong khi thật là 197 → luôn dùng syllables.py.
- Sửa lời đọc nhưng chữ trên màn còn ý cũ.
- Promise hứa 2 điều, payoff chỉ trả lời 1.

## Mẫu ghi điểm (cuối script.md)

```
> Âm tiết: 232 (mục tiêu 215–250) · file thật 59,1 s
> Chấm: Hook 4 (câu hỏi rõ, thiếu yếu tố bất ngờ) · Lời hứa 5 (nêu đúng 2 điều sẽ biết) · Một ý 5 · Dễ hiểu 4 ("host" vẫn là từ Anh) · Chính xác 5 (10/10 câu có trích dẫn) · Hình 4 (cảnh step3 hơi thưa) · Đóng vòng 5 · Độ dài 5
> 3 điểm yếu lớn nhất: 1) … 2) … 3) …
```
