# Prompt: trích "ý làm được video" từ một nguồn

**Dùng khi:** có một nguồn mới (chapter sách, bài báo, paper, văn bản dán). Đầu ra là danh sách ý để chọn và viết kịch bản bằng `prompts/script.md`.

**Đọc trước:** `style/style_bible.md`, `style/lessons.md`.

---

## Đầu vào

- `SOURCE`: toàn văn nguồn (hoặc phần cần làm). Ghi rõ cách đánh dấu vị trí: số trang cho PDF/sách, số đoạn (¶1, ¶2…) cho bài web.
- `SOURCE_META`: tên, tác giả, năm, lĩnh vực, link (nếu có).
- `N`: số ý muốn lấy (mặc định 8–12 với chapter/paper, 4–6 với bài báo ngắn).

## Việc cần làm

1. Đọc hết nguồn. Đánh số đoạn nếu nguồn chưa có số trang.
2. Liệt kê mọi ý có thể thành **một video 45–90 giây trả lời một câu hỏi**. Một ý tốt:
   - trả lời được một câu hỏi người thường **từng tự hỏi** hoặc **sẽ tò mò khi nghe**;
   - có ít nhất một **bằng chứng cụ thể** trong nguồn (số liệu, thí nghiệm, ví dụ, trích dẫn);
   - giải thích được trong 2–3 bước, không cần kiến thức nền dài;
   - đứng một mình được (không bắt người xem phải xem phần trước).
3. Loại ý chỉ là định nghĩa, tóm tắt chung chung, hoặc không có bằng chứng trong nguồn.
4. Với mỗi ý, điền đủ các trường ở mẫu dưới. **Bằng chứng phải trích nguyên văn** (tiếng gốc), kèm trang/đoạn. Không có trích dẫn thì không được đưa ý vào.
5. Chấm **Điểm hấp dẫn 1–5** cho người lướt TikTok không quan tâm chủ đề:
   - 5: chạm thói quen/nỗi đau hằng ngày, có kết quả bất ngờ hoặc con số mạnh;
   - 3: thú vị với người tò mò, cần lời hứa tốt mới giữ được;
   - 1: chỉ người trong ngành quan tâm.
6. Sắp xếp theo điểm hấp dẫn giảm dần. Đề xuất **thứ tự series** (ý nào làm Phần 1 để kéo người xem, các phần sau nối nhau ra sao).

## Mẫu đầu ra (`videos/<series>/ideas.md`)

```markdown
# Ý video: <tên nguồn>
Nguồn: <tác giả>, <tên>, <năm>. Lĩnh vực: <...>. Series: <tên series ngắn>

## Ý 1 — <tên ngắn>
- **Câu hỏi hook:** <câu hỏi người xem tự hỏi, dưới 12 âm tiết khi đọc>
- **Trả lời một câu:** <câu trả lời mà nhịp 5 sẽ nói>
- **Khái niệm nền (nếu có):** <thuật ngữ cần giải thích, một câu>
- **2–3 bước giải thích:** 1) … 2) … 3) …
- **Ví dụ đời thường:** <tình huống người Việt quen>
- **Bằng chứng:**
  - "<trích nguyên văn>" (tr. 45 / ¶12)
  - "<trích nguyên văn>" (tr. 47)
- **Điểm hấp dẫn:** 4/5 — <một dòng lý do>
- **Rủi ro chính xác:** <chỗ dễ nói quá so với nguồn, nếu có>

## Thứ tự series đề xuất
1. Ý 3 (Phần 1) — lý do
2. ...
```

## Luật

- Không thêm kiến thức ngoài nguồn vào phần "Bằng chứng". Kiến thức chung (ví dụ đời thường) được phép nhưng không được trình bày như phát hiện của nguồn.
- Nguồn nói "có thể", "ở nhóm sinh viên Mỹ", "trong một thí nghiệm" thì giữ nguyên mức độ đó, ghi ở "Rủi ro chính xác".
- Paper: ưu tiên kết quả chính (abstract, results), ghi rõ cỡ mẫu và đối tượng.
