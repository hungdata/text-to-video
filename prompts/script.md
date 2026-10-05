# Prompt: viết kịch bản từ một ý

**Dùng khi:** đã có một ý trong `videos/<series>/ideas.md`. Đầu ra là `script.md` (cú pháp explainroo) + `source.md` + phần tự chấm.

**Đọc trước:** `style/style_bible.md`, `style/lessons.md`, và ý cần viết trong `ideas.md`.

---

## Đầu vào

- `IDEA`: một mục trong ideas.md (câu hỏi hook, trả lời, bước, bằng chứng).
- `SERIES`: tên series, số phần (Phần n), phần tiếp theo là gì (nếu biết).
- `LENGTH`: mặc định 60 s (215–250 âm tiết). 45 s: 165–185. 90 s: 330–370.

## Các bước

1. **Viết 3 phương án hook**, mỗi phương án một mẫu khác nhau (style bible mục 4). Mỗi phương án đủ 3 lớp:
   - lời đọc (dưới 12 âm tiết),
   - chữ trên màn (3–7 chữ),
   - hình đầu tiên có chuyển động (mô tả bằng một câu).
   Chọn phương án mạnh nhất cho script, ghi lý do.
2. **Viết lời đọc** theo khung 6 nhịp, mỗi nhịp một `## scene-id`:
   `hook`, `promise`, `concept` (bỏ nếu không có thuật ngữ), `step1`, `step2`, (`step3` nếu 90 s), `payoff`, `outro`.
3. **Đặt `[#mốc]`** trước cụm từ cần minh họa. Câu nào cũng có ít nhất một mốc. Tên mốc ngắn, không dấu (`[#late]`, `[#bars]`).
4. **Số và từ ngoại** viết bằng `{hiển thị|cách đọc}` (style bible mục 6).
5. **Ghi chú hình** dưới mỗi cảnh bằng dòng `>` (không đọc): mỗi mốc hiện hình gì, ở đâu, màu gì. Giữ tối đa 5–6 vật trên màn.
6. **Đếm âm tiết** bằng `python3 .agents/skills/text-to-video-vi/scripts/syllables.py videos/<slug>/script.md` (đếm phần "cách đọc" trong `{|}`, bỏ dòng `>`). Ngoài khoảng `LENGTH` thì sửa. Ghi đúng con số máy đếm, không ước chừng.
7. **Viết `source.md`**: với mỗi số liệu hoặc khẳng định trong lời đọc, dán câu lời đọc + trích nguyên văn nguồn + trang/đoạn.
8. **Tự chấm** theo `resources/review_rubric.md` (8 tiêu chí, mỗi điểm kèm bằng chứng, bắt buộc nêu 3 điểm yếu). Tiêu chí nào dưới 4 thì viết lại phần đó và chấm lại (tối đa 2 vòng). Ghi điểm cuối cùng ở cuối script.md.
9. Rà lần cuối với **cụm cấm** và **lessons.md**.

## Mẫu `script.md`

```markdown
# <Câu hỏi hook làm tiêu đề>

> Series: <Lĩnh vực> · <Tên series> · Phần <n>
> Nguồn: <tác giả>, <tên>, <năm>
> Hook đã chọn: B (Kết quả trước) — lý do: ...
> Hook A (<mẫu>): lời "…" | chữ "…" | hình: …
> Hook B (<mẫu>): lời "…" | chữ "…" | hình: …
> Hook C (<mẫu>): lời "…" | chữ "…" | hình: …

## hook {hold=0.4}
[#q] <câu hook>.
> [#q] tiêu đề "<3–7 chữ>" enter none; <hình chuyển động>

## promise
[#problem] <vấn đề>. [#promise] Trong một phút, bạn sẽ biết <lời hứa>.
> [#problem] …; [#promise] …; tên nguồn nhỏ dưới tiêu đề

## concept
...

## step1
... [#hook2] Nhưng còn một lý do sâu hơn.

## step2
...

## payoff {hold=1.2}
[#answer] <một câu trả lời rõ ràng cho câu hỏi hook>.
> sơ đồ hiện lại, ý chính tô màu nhấn

## outro {hold=1.5}
[#apply] Lần tới khi <tình huống>, <hành động>. [#next] <mời Phần sau hoặc câu hỏi bình luận>.

> ---
> Âm tiết: 232 (mục tiêu 215–250) · ước lượng 59 s
> Chấm: Hook 5 · Lời hứa 5 · Một ý 5 · Dễ hiểu 4 (thuật ngữ "x" vẫn hơi khó) · Chính xác 5 · Hình 5 · Đóng vòng 5 · Độ dài 5
> Tóm một câu: <...>
```

## Luật

- Câu hỏi ở `hook` phải được trả lời **nguyên vẹn** ở `payoff`. Đọc `hook` rồi đọc `payoff` liền nhau phải thành một cặp hỏi–đáp.
- Không đưa vào lời đọc bất kỳ số liệu nào không có trong `source.md`.
- Không dùng tên nguồn trong `hook`.
- `outro` không được có "follow", "like", "đăng ký".
