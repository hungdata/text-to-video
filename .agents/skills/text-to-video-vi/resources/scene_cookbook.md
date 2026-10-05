# Sổ tay vẽ cảnh (scenes.js) cho TikTok tiếng Việt

Tài liệu đầy đủ của Scene API: `engine/explainroo-mac/AGENTS.md`, mục "Scene API". File này là phần rút gọn + các bẫy đã gặp thật.

## 1. Khung hình TikTok (size "tiktok", 1080×1920)

| Vùng | Toạ độ |
|---|---|
| Vùng an toàn `s.safe` | x 119 → 864, y 304 → 1050 (745×746) |
| Tâm `s.cx`, `s.cy` | ≈ 491, ≈ 677 |
| Phụ đề tự động | y ≈ 1074 → 1257 (dưới vùng an toàn) |
| Watermark | góc trên phải |
| Phần dưới y 1257 | nút + tên + caption của TikTok che: để trống là ĐÚNG |

Đặt mọi thứ tính từ `const top = s.safe.y;`:

- Dải tiêu đề: `top + 80` → `top + 200` (chữ display 76–92 px).
- Dải hình chính: `top + 250` → `top + 620`.
- Dải phụ / khung lời mời: `top + 620` → `top + 700` (không quá `top + 720`).
- Hai cột: trái `x = s.safe.left + 170`, phải `x = s.safe.right - 170`.

Cỡ chữ: tiêu đề 76–92; nhãn 44–56; ghi chú ≥ 36. Danh sách 42–52.

## 2. Bẫy đã gặp (đọc kỹ)

1. **Hẹn giờ theo chữ có dấu hay hỏng.** `s.cue('mười ba')` báo lỗi vì engine bỏ dấu khi so. LUÔN đặt `[#ten]` trong script.md và dùng `at: '#ten'` hoặc `s.time('#ten') + 0.5`.
2. **`s.annotate({ x, y, w, h })`: x, y là TÂM của khung**, không phải góc trên trái.
3. **Ảnh (`s.image`, có `h`)**: chiều rộng hiển thị có thể khác bạn tính. Muốn khoanh một chỗ trên ảnh: render `still` trước, đo toạ độ trên PNG, rồi đặt `annotate` theo độ lệch so với tâm ảnh (`ix + dx`, `iy + dy`). Kiểm tra lại bằng still.
4. **Danh sách xuống hàng giữa chừng** ("chỉnh tùy\ný"): thêm `width: 700–730` cho `s.list`, giảm `size`, hoặc rút chữ. `gap` ≥ 2 × `size`.
5. **`bullet` chỉ nhận** `dot`, `dash`, `number`, `check`, `arrow` hoặc tên icon. `'none'` = LỖI (engine coi là icon).
6. **`s.box` có `icon` thành thẻ cao (~180 px)** và dễ xuống hàng. Chật chỗ thì bỏ icon trong box, vẽ icon riêng; thêm `w: 600–680` để chữ không xuống hàng.
7. **Tô màu chữ trong danh sách** (`color` trên từng mục) → check báo "low contrast". Giữ chữ màu mực, tô màu icon/bullet (`bulletColor`).
8. **Vật có y > 1050** → WARN "caption band". Kéo lên.
9. **Chữ trong khung mời đè lên danh sách**: tính chiều cao box (~100 px không icon, ~180 px có icon) khi chọn y.
10. **Quên sửa `video.json` khi sao chép** (title vẫn là video cũ). Luôn sửa title.
11. **Icon không tồn tại** → lỗi. Tìm trước: `node engine/explainroo-mac/bin/explainroo.js icons <từ tiếng Anh>`.
12. **Cảnh quá thưa** (2–3 icon nhỏ giữa nền trống) trông rẻ tiền: mỗi cảnh nên có một hình chính to (icon 140–200 px, sơ đồ, ảnh thật, biểu đồ) + 1–3 nhãn.
13. **Sửa nội dung lời đọc thì sửa cả hình**: dòng chữ trên màn hình từ bản kịch bản cũ còn sót là lỗi rất dễ gặp (vd. lời hứa đã đổi nhưng danh sách trên màn vẫn ghi ý cũ). Sau mỗi lần sửa script, grep lại scenes.js.

## 3. Công thức hay dùng

```js
// Tiêu đề hook có sẵn từ khung đầu (ảnh bìa)
s.text('Gas trong bình\nlà *chất lỏng*', { font: 'display', size: 84, y: top + 110, enter: 'none', at: 0 });

// Danh sách hiện theo từng mốc
s.list([
  { text: 'Lửa lên ngay, chỉnh tùy ý', icon: 'flame', at: '#fast' },
  { text: 'Mất điện vẫn nấu', icon: 'zap-off', at: '#power' },
], { x: s.safe.left + 10, y: top + 220, size: 50, gap: 120, width: 730, bulletColor: 'accent' });

// Hai hộp nối mũi tên
s.box('Host · Claude', { id: 'host', x: s.cx, y: top + 120, size: 56, icon: 'bot', color: 'blue', at: '#host' });
s.box('Lịch', { id: 'sv1', x: s.safe.left + 170, y: top + 560, size: 52, color: 'accent', at: '#server' });
s.arrow('host', 'sv1', { at: '#client', label: 'đường riêng', labelSize: 36 });

// Ảnh sản phẩm thật (PNG đã tách nền) + khoanh một chi tiết (x, y của annotate là TÂM)
const ix = s.safe.left + 165, iy = top + 360;            // tâm ảnh
s.image('assets/san-pham.png', { x: ix, y: iy, h: 520, shadow: false, at: 0.1 });
// dx, dy = vị trí chi tiết trừ tâm ảnh, ĐO trên still đã render (không tính bằng tay)
s.annotate({ x: ix + 99, y: iy - 81, w: 84, h: 52 }, { type: 'circle', color: 'red', at: s.time('#chitiet') + 0.5 });

// Vật nối tiếp từ cảnh trước (không vẽ lại, không có tiếng)
s.icon('bot', { x: s.cx, y: top + 230, size: 150, color: 'blue', at: -1 });

// Biểu đồ cột
s.bars([{ label: 'Dự đoán', value: 3, color: 'blue' }, { label: 'Thực tế', value: 7, color: 'red' }],
  { x: s.cx, y: top + 430, w: 600, h: 300, values: false, at: '#bars', stagger: 0.6 });
```

Vẽ tự do bằng canvas (`s.draw`): xem hàm `tank()` trong `examples/gas-01-binh-gas/scenes.js` (bình có chất lỏng gợn sóng, van xoay, bọt hơi). Trong `s.draw`, toạ độ tính từ `x, y` đã cho; dùng `s.T` cho chuyển động liên tục, `s.rand(i)` cho ngẫu nhiên cố định.

## 4. Nhịp hình

- Mỗi 2–4 giây có một thay đổi (vật mới, mũi tên, khoanh, đổi màu). HINT "no new element for Xs" = cảnh đứng quá lâu: thêm một chi tiết theo mốc.
- Tối đa 5–6 vật cùng lúc; dùng `out: '#moc'` để dọn trước ý mới.
- Một màu cho một nghĩa suốt video; `accent` chỉ cho điều quan trọng nhất.
- Khung cuối phải rõ ý chính (người xem hay dừng ở đó).

## 5. Ảnh sản phẩm của người dùng

```bash
python3 .agents/skills/text-to-video-vi/scripts/remove_bg.py <ảnh gốc> --find-holes
python3 .agents/skills/text-to-video-vi/scripts/remove_bg.py <ảnh gốc> videos/<slug>/assets/san-pham.png \
  --seed X,Y --preview /tmp/xem.jpg
```

Mở `/tmp/xem.jpg` nhìn: không còn nền trắng quanh vật, nhãn dán/chữ trắng trên vật còn nguyên.
