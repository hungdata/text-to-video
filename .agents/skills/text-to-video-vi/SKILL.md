---
name: text-to-video-vi
description: "Make a Vietnamese TikTok video (9:16, 45-90 s, male voice vi-VN-NamMinhNeural, hand-drawn animated scenes, word-synced captions) end to end on this Mac with explainroo: research and verify sources, write the script, draw the scenes, generate the voice, check, and render to samples/. Two kinds: explainers ('X là gì', 'vì sao...', from a topic, link, book, paper or pasted text) and product or sales videos for a shop or dealer (with the user's product photo). Use whenever the user asks to làm video, tạo video TikTok, video giải thích, video giới thiệu sản phẩm, video bán hàng, sửa hoặc render lại một video, or gives a topic, link or photo to turn into a video."
---

# Làm video TikTok tiếng Việt từ đầu đến cuối

Bạn tự làm trọn một video: từ yêu cầu của người dùng đến file MP4 trong `samples/`, ngay trên Mac này.
Chuẩn chất lượng là hai video người dùng đã duyệt: `examples/mcp-01-la-gi` (giải thích) và `examples/gas-01-binh-gas` (bán hàng).
Đọc cả 4 file của video mẫu cùng loại trước khi viết video mới.

Chạy mọi lệnh từ thư mục dự án (workspace) `~/Desktop/book-to-video`. Trong file này `SK` = `.agents/skills/text-to-video-vi`.

## 0. Kiểm tra bộ dựng (một lần mỗi phiên)

```bash
bash .agents/skills/text-to-video-vi/scripts/setup_mac.sh
```

Phải thấy `SETUP OK` ở dòng cuối. Có dòng `LỖI:` thì sửa đúng lỗi đó (cài Node/ffmpeg, tắt VPN hoặc đổi mạng) rồi chạy lại. Không làm tiếp khi chưa có `SETUP OK`.
Hai dòng `FAIL voice model` và `FAIL speech check model` của doctor là bình thường.

## 1. Hiểu yêu cầu

Cần biết:
- **Loại**: A = giải thích; B = bán hàng / giới thiệu sản phẩm.
- **Chủ đề** và **nguồn** (link, file). Người dùng không đưa nguồn thì tự tìm nguồn uy tín.
- **Độ dài**: mặc định 60 giây.
- Loại B: **ảnh sản phẩm** (nhờ người dùng bỏ file vào workspace), **tên + số điện thoại đại lý** (chưa có thì để khung chữ chung, không bịa).
- Điều người dùng muốn nhấn mạnh hoặc bỏ.

Hỏi người dùng tối đa một lần, gộp các câu hỏi lại. Chi tiết không quan trọng thì dùng mặc định và ghi rõ trong báo cáo.

## 2. Đọc trước khi viết (bắt buộc)

1. `style/style_bible.md` (không có thì dùng `SK/resources/style_bible.md`): giọng văn, khung nhịp, cụm cấm, cách viết số, mục 10 cho video bán hàng.
2. `style/lessons.md`: luật rút từ góp ý của người dùng. **Thắng style bible** khi mâu thuẫn.
3. `SK/resources/prompt_script.md`. Nguồn dài (chapter, paper) thì làm `SK/resources/prompt_extract.md` trước để chọn ý.
4. `SK/resources/scene_cookbook.md`: khung hình TikTok và **các bẫy đã gặp thật**.
5. Video mẫu cùng loại trong `SK/examples/`.

## 3. Nguồn và kiểm chứng

- Mở nguồn thật (trình duyệt hoặc tải trang). Chép trích dẫn **nguyên văn** vào `source.md` ngay lúc đọc, không viết từ trí nhớ.
- Ưu tiên: tài liệu chính thức, Wikipedia, trang nhà nước / tiêu chuẩn, nhà sản xuất hoặc đại lý chính thức (cho thông số sản phẩm).
- Ý nào không tìm được nguồn thì bỏ ý đó. Ví dụ: video gas đã bỏ "van an toàn xả áp" vì không có nguồn cho bình 12 kg dân dụng.

## 4. Tạo thư mục video và viết

```bash
ls videos/
bash .agents/skills/text-to-video-vi/scripts/new_video.sh <slug> "<Tiêu đề>"
```

`slug` = `<series>-<số>-<tên không dấu>`, ví dụ `ai-03-llm-la-gi`, `gas-02-doi-gas-an-toan`. Không trùng thư mục đã có.

Viết theo thứ tự:
1. `script.md`: 3 phương án hook (3 lớp), khung nhịp, `[#mốc]` ở **mọi câu**, `{hiển thị|cách đọc}` cho số và từ ngoại.
2. `source.md`: mỗi khẳng định một dòng, kèm trích dẫn nguyên văn.
3. `scenes.js`: theo cookbook và video mẫu. Hẹn giờ bằng `'#mốc'`, mọi vật trong `s.safe`.
4. `video.json`: **sửa `title`**.

Ảnh sản phẩm: tách nền theo cookbook mục 5, lưu vào `videos/<slug>/assets/`.

## 5. Dựng nháp và NHÌN

```bash
bash .agents/skills/text-to-video-vi/scripts/build.sh <slug>
```

- Độ dài phải `ĐẠT` (trừ khi người dùng yêu cầu độ dài khác).
- Check phải sạch `ERROR`/`WARN`. Mã thoát 2 nghĩa là chưa sạch.
- **Mở và nhìn** `videos/<slug>/out/sheet.jpg` và từng `videos/<slug>/out/stills/<cảnh>@end.png`. Soát: chữ đủ dấu, không đè nhau, không bị cắt, không xuống hàng xấu, khoanh và mũi tên trúng chỗ, mỗi cảnh có một hình chính rõ.
- Sửa rồi chạy lại `build.sh`. Giọng chỉ được tạo lại cho cảnh có lời đã đổi.

## 6. Tự chấm trung thực

Theo `SK/resources/review_rubric.md`: mỗi điểm kèm bằng chứng, bắt buộc nêu **3 điểm yếu lớn nhất**, không cho 5/5 cả 8 tiêu chí ở bản đầu.
Tiêu chí nào ≤ 3 thì sửa (tối đa 2 vòng). Ghi điểm và điểm yếu ở cuối `script.md`.

## 7. Render

```bash
bash .agents/skills/text-to-video-vi/scripts/build.sh <slug> --render --safe
```

> **QUY TẮC AN TOÀN TÀI NGUYÊN (Worker Throttling - Chống Đơ Máy):**
> - Trên máy Mac 8GB RAM, luôn thêm cờ `--safe` (hoặc để tự động nhận diện 1 worker). `build.sh` đã tự động phát hiện RAM ≤ 8GB và gán QoS `taskpolicy -c utility` để bảo vệ giao diện macOS, đảm bảo con trỏ chuột và ứng dụng nền không bị đơ giật.
> - Chạy 1 worker chỉ tốn ~600MB RAM (thay vì 3.5GB với 4 worker), render cực nhanh (~30 giây) mà không bị nghẽn bộ nhớ. TUYỆT ĐỐI không render nhiều video cùng lúc.

Kết quả: `samples/<slug>.mp4` (bản gốc để đăng) và `samples/<slug>_preview.mp4` (bản nhẹ để gửi xem). Đọc dòng `Thời lượng · Khổ · Âm lượng`: khổ phải 1080x1920, mean_volume khoảng -14 đến -20 dB.
Không dùng lệnh `verify` của explainroo: nó kiểm tra bằng nhận dạng giọng tiếng Anh.

## 8. Báo cáo cho người dùng (ngắn)

- File: `samples/<slug>.mp4`, thời lượng.
- Câu hook và một câu tóm nội dung.
- Điểm chấm và 3 điểm yếu.
- Nguồn đã dùng (link).
- Việc cần người dùng quyết (ví dụ: tên + SĐT đại lý, tên kênh để thay watermark).

Không tự đăng lên TikTok.

## 9. Góp ý của người dùng

- Mỗi góp ý thành **một luật cụ thể** trong `style/lessons.md`. Đọc lại file ngay trước khi ghi, chỉ thêm dòng mới.
- Sửa video theo góp ý rồi build lại.
- Bỏ một phần nội dung: sửa cả `promise` và `payoff` cho khớp, rồi tìm chữ cũ còn sót trong `scenes.js` (`grep -n "<chữ cũ>" videos/<slug>/scenes.js`).

## Chạy nhiều Antigravity cùng lúc

- Mỗi agent làm một video (một slug riêng). Không sửa thư mục video của agent khác.
- `engine/explainroo-mac` dùng chung và chỉ đọc. Chỉ một agent chạy `setup_mac.sh` lần đầu.
- Máy chủ giọng giới hạn tốc độ: tối đa 2–3 agent tạo giọng cùng lúc. `voice_vi.py` tự thử lại 4 lần khi bị từ chối (`NoAudioReceived`). Vẫn lỗi thì đợi 3–5 phút rồi chạy lại `build.sh`; câu đã có được giữ.
- Render tốn CPU: tối đa 2 render cùng lúc.
- `style/lessons.md` dùng chung: đọc lại ngay trước khi thêm dòng.

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|---|---|
| `NoAudioReceived`, lỗi mạng khi tạo giọng | Đợi 3–5 phút, tắt VPN hoặc đổi mạng, chạy lại `build.sh` |
| `cue("...") is not in the narration` | Dùng `[#mốc]` trong script.md và `at: '#mốc'` |
| `icon "x" does not exist` | `node engine/explainroo-mac/bin/explainroo.js icons <từ tiếng Anh>` |
| `WARN ... caption band` / `outside the tiktok safe area` | Kéo vật vào trong `s.safe` (y ≤ 1050, x 119–864) |
| `low contrast` | Bỏ `color` ở chữ, tô màu icon hoặc `bulletColor` |
| Chữ trong list/box xuống hàng xấu | `width` cho list, `w` cho box, giảm `size` hoặc rút chữ |
| `HINT no new element for Xs` | Thêm một chi tiết theo mốc trong quãng đó |

## Các file trong skill

| File | Dùng để |
|---|---|
| `scripts/setup_mac.sh` | Cài / kiểm tra bộ dựng, thư viện, mạng, giọng thử |
| `scripts/new_video.sh` | Tạo `videos/<slug>/` từ mẫu |
| `scripts/build.sh` | Độ dài → giọng → check → ảnh khung hình; `--render` để xuất MP4 |
| `scripts/syllables.py` | Đếm âm tiết, ước lượng thời lượng (~235 âm tiết/phút) |
| `scripts/remove_bg.py` | Tách nền trắng ảnh sản phẩm (`--find-holes` tìm vùng trắng kín) |
| `scripts/voice_vi.py` | Giọng NamMinh có tự thử lại (setup chép vào bộ dựng) |
| `resources/style_bible.md` | Luật viết của kênh (bản dự phòng; ưu tiên `style/` trong workspace) |
| `resources/prompt_extract.md`, `prompt_script.md` | Các bước trích ý và viết kịch bản |
| `resources/scene_cookbook.md` | Khung hình, công thức vẽ, các bẫy đã gặp |
| `resources/review_rubric.md` | Bảng chấm trung thực + kiểm tra máy móc |
| `resources/template/` | Mẫu 4 file cho video mới |
| `examples/` | Hai video đã được duyệt |
