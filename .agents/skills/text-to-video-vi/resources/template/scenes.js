// {{TITLE}} — vùng an toàn TikTok: 745×746 tại (119, 304); s.cx ≈ 491; dưới y 1050 là phụ đề + nút TikTok.
// Quy tắc: mọi vật trong s.safe; tiêu đề hook enter 'none'; ≤ 5–6 vật/cảnh; 2–4 giây có một thay đổi;
// hẹn giờ bằng mốc '#ten' (KHÔNG dùng s.cue('chữ có dấu')). Xem resources/scene_cookbook.md.
export default {
  hook(s) {
    const top = s.safe.y;
    s.text('Tiêu đề\n*3–7 chữ*', { font: 'display', size: 88, y: top + 120, enter: 'none', at: 0 });
    s.icon('sparkles', { x: s.cx, y: top + 450, size: 200, color: 'accent', at: '#q', float: 6 });
  },

  promise(s) {
    const top = s.safe.y;
    s.icon('circle-help', { x: s.cx, y: top + 160, size: 150, color: 'orange', at: '#problem' });
    s.list([
      { text: 'Lời hứa thứ nhất', icon: 'check', at: '#promise' },
    ], { x: s.safe.left + 20, y: top + 380, size: 52, gap: 110, width: 720 });
  },

  concept(s) {
    const top = s.safe.y;
    s.text('*Thuật ngữ*', { id: 'term', font: 'display', size: 120, y: top + 220, at: '#term', enter: 'pop' });
    s.note('giải thích ngắn', { x: s.cx, y: top + 400, size: 44, at: '#def' });
  },

  step1(s) {
    const top = s.safe.y;
    s.box('Bước 1', { id: 'a', x: s.cx, y: top + 200, size: 56, icon: 'footprints', color: 'blue', at: '#s1' });
    s.text('?', { font: 'display', size: 120, x: s.safe.right - 60, y: top + 120, color: 'accent', at: '#hook2', enter: 'pop' });
  },

  step2(s) {
    const top = s.safe.y;
    s.box('Bước 2', { id: 'b', x: s.cx, y: top + 400, size: 56, icon: 'footprints', color: 'teal', at: '#s2' });
  },

  payoff(s) {
    const top = s.safe.y;
    s.text('Câu trả lời\n*ý chính*', { font: 'display', size: 84, y: top + 220, at: '#answer' });
  },

  outro(s) {
    const top = s.safe.y;
    s.text('Tóm ý chính', { font: 'display', size: 76, y: top + 200, at: '#apply' });
    s.box('Phần sau: …', { x: s.cx, y: top + 600, size: 46, color: 'gray', dashed: true, at: '#next' });
  },
};
