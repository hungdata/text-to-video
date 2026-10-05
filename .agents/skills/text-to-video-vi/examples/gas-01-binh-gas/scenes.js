// Bình gas hoạt động thế nào? — video bán hàng đại lý. Vùng an toàn TikTok: 745×746 tại (119, 304).
const IMG = 'assets/binh-gas.png'; // 409×729 sau khi tách nền
const IMG_W = 409, IMG_H = 729;

// Sơ đồ bình gas: vỏ thép, gas lỏng gợn sóng, van trên đỉnh, bọt hơi khi van mở.
function tank(s, { x, y, at = 0, openAt = null, liquidColor = 'blue', w = 230, h = 380 }) {
  const ink = s.color('ink');
  const liq = s.color(liquidColor);
  const liqTint = s.tint(liquidColor);
  s.draw({ x, y, at }, (ctx, life) => {
    const p = life.p;
    ctx.save();
    ctx.globalAlpha = Math.min(1, p * 1.5);
    const r = 60, L = -w / 2, T = -h / 2;
    // thân bình
    ctx.beginPath();
    ctx.roundRect(L, T, w, h, r);
    ctx.lineWidth = 6; ctx.strokeStyle = ink; ctx.stroke();
    // gas lỏng: 55% dưới, mặt sóng
    ctx.save();
    ctx.beginPath(); ctx.roundRect(L + 5, T + 5, w - 10, h - 10, r - 5); ctx.clip();
    const level = T + h * 0.45;
    ctx.beginPath();
    ctx.moveTo(L, h / 2);
    for (let i = 0; i <= 40; i++) {
      const xx = L + (w * i) / 40;
      ctx.lineTo(xx, level + Math.sin(i / 3 + s.T * 3) * 6);
    }
    ctx.lineTo(L + w, h / 2); ctx.closePath();
    ctx.fillStyle = liqTint; ctx.fill();
    ctx.lineWidth = 4; ctx.strokeStyle = liq; ctx.stroke();
    // bọt hơi bay lên khi van mở
    if (openAt !== null && s.T >= openAt) {
      const k = s.T - openAt;
      for (let i = 0; i < 9; i++) {
        const ph = (k * 0.9 + s.rand(i)) % 1;
        const bx = L + 30 + s.rand(i + 20) * (w - 60);
        const by = level - ph * (h * 0.4) + 10;
        ctx.beginPath(); ctx.arc(bx, by, 7 + 5 * s.rand(i + 40), 0, Math.PI * 2);
        ctx.lineWidth = 3; ctx.strokeStyle = liq; ctx.globalAlpha = 1 - ph; ctx.stroke(); ctx.globalAlpha = 1;
      }
    }
    ctx.restore();
    // van
    const open = openAt !== null && s.T >= openAt ? Math.min(1, (s.T - openAt) / 0.4) : 0;
    ctx.fillStyle = ink;
    ctx.fillRect(-18, T - 40, 36, 40);
    ctx.save(); ctx.translate(0, T - 52); ctx.rotate(open * Math.PI / 2);
    ctx.fillRect(-34, -8, 68, 16); ctx.restore();
    ctx.restore();
  });
}

export default {
  hook(s) {
    const top = s.safe.y;
    s.text('Gas trong bình\nlà *chất lỏng*', { font: 'display', size: 84, y: top + 110, enter: 'none', at: 0 });
    s.image(IMG, { x: s.safe.left + 180, y: top + 490, h: 470, shadow: false, at: 0, enter: 'none', float: 4 });
    tank(s, { x: s.safe.right - 180, y: top + 500, w: 200, h: 320, at: '#liquid' });
    s.arrow([s.safe.left + 340, top + 500], [s.safe.right - 300, top + 500], { at: s.time('#liquid') + 0.2, dashed: true });
  },

  promise(s) {
    const top = s.safe.y;
    s.icon('flame', { x: s.cx - 90, y: top + 150, size: 150, color: 'orange', at: '#why' });
    s.text('?', { font: 'display', size: 170, x: s.cx + 90, y: top + 150, color: 'accent', at: s.time('#why') + 0.3, enter: 'pop' });
    s.list([
      { text: 'Bình gas làm việc ra sao', icon: 'circle-help', at: '#promise' },
      { text: 'Vì sao an toàn', icon: 'shield-check', at: '#enough' },
    ], { x: s.safe.left + 20, y: top + 380, size: 50, gap: 100, width: 720 });
  },

  concept(s) {
    const top = s.safe.y;
    tank(s, { x: s.safe.left + 170, y: top + 420, at: '#press' });
    s.text('Áp suất\n*cao*', { font: 'display', size: 64, x: s.safe.left + 170, y: top + 110, at: s.time('#press') + 0.4 });
    s.box('1', { id: 'one', x: s.safe.right - 260, y: top + 300, w: 70, h: 70, size: 40, color: 'blue', at: '#ratio' });
    s.box('250', { id: 'many', x: s.safe.right - 130, y: top + 540, w: 210, h: 210, size: 64, color: 'teal', fillStyle: 'dots', at: s.time('#ratio') + 0.8 });
    s.arrow('one', 'many', { at: s.time('#ratio') + 0.5, bend: 0.3, label: 'nở ra', labelSize: 40 });
    s.note('lỏng : hơi', { x: s.safe.right - 130, y: top + 690, size: 38, at: s.time('#ratio') + 1.0 });
  },

  step1(s) {
    const top = s.safe.y;
    const tx = s.safe.left + 170, ty = top + 440;
    tank(s, { x: tx, y: ty, at: -1, openAt: s.T - s.t + s.time('#boil') });
    s.note('mở van', { x: tx, y: top + 140, size: 40, color: 'accent', at: '#valve' });
    s.icon('flame', { id: 'fire', x: s.safe.right - 150, y: top + 220, size: 160, color: 'orange', at: '#flame', label: 'bếp', labelSize: 44 });
    s.arrow([tx + 40, ty - 250], 'fire', { at: '#pipe', bend: -0.4, label: 'dây dẫn', labelSize: 38 });
    s.text('lỏng → *hơi*', { font: 'display', size: 60, x: s.safe.right - 170, y: top + 600, at: '#boil' });
  },

  step2(s) {
    const top = s.safe.y;
    s.text('Lợi ích', { font: 'display', size: 84, y: top + 80, at: 0.1 });
    s.list([
      { text: 'Lửa lên ngay, chỉnh tùy ý', icon: 'flame', at: '#fast' },
      { text: 'Ít bụi muội hơn dầu hỏa', icon: 'sparkles', at: '#clean' },
      { text: 'Mất điện vẫn nấu', icon: 'zap-off', at: '#power' },
    ], { x: s.safe.left + 10, y: top + 220, size: 50, gap: 120, width: 730, bulletColor: 'accent' });
  },

  safe1(s) {
    const top = s.safe.y;
    const ih = 520, ix = s.safe.left + 165, iy = top + 360;
    s.image(IMG, { x: ix, y: iy, h: ih, shadow: false, at: 0.1 });
    // quai bình: thanh ngang trên cùng của ảnh (đo trên khung đã render, ảnh h 460 → quy đổi)
    const k = ih / 460;
    s.annotate({ x: ix + 16 * k, y: iy - 215 * k, w: 190 * k, h: 50 * k }, { type: 'circle', color: 'red', at: '#handle' });
    s.list([
      { text: 'Thép chuyên dụng', icon: 'shield-check', at: '#steel' },
      { text: 'Kiểm định ~5 năm', icon: 'calendar-check', at: '#check' },
      { text: 'Hạn ghi trên quai', icon: 'tag', at: '#handle' },
    ], { x: s.cx - 60, y: top + 160, size: 42, gap: 150, width: 520, bulletColor: 'accent' });
  },

  safe2(s) {
    const top = s.safe.y;
    s.icon('wind', { x: s.cx, y: top + 110, size: 140, color: 'purple', at: '#smell' });
    s.box('Mùi hôi = có rò rỉ', { x: s.cx, y: top + 270, size: 50, color: 'red', at: s.time('#smell') + 0.6 });
    s.icon('badge-check', { x: s.cx, y: top + 470, size: 140, color: 'green', at: '#seal' });
    s.box('Màng co + tem chống giả', { x: s.cx, y: top + 630, size: 44, w: 640, color: 'green', at: s.time('#seal') + 0.6 });
  },

  payoff(s) {
    const top = s.safe.y;
    const tx = s.safe.left + 170, ty = top + 440;
    tank(s, { x: tx, y: ty, at: '#answer', liquidColor: 'accent', openAt: s.T - s.t + s.time('#open') });
    s.text('lỏng nhờ\n*áp suất*', { font: 'display', size: 64, x: s.safe.right - 180, y: top + 200, at: s.time('#answer') + 0.4 });
    s.icon('flame', { id: 'f2', x: s.safe.right - 180, y: top + 400, size: 130, color: 'orange', at: '#open', label: 'mở van mới cháy', labelSize: 40 });
    s.box('An toàn', { x: s.safe.right - 180, y: top + 650, size: 50, color: 'green', at: '#safe' });
    s.icon('shield-check', { x: s.safe.left + 170, y: top + 440, size: 300, color: 'green', weight: 1.5, at: '#safe', opacity: 0.35 });
  },

  outro(s) {
    const top = s.safe.y;
    const ih = 460, ix = s.safe.left + 165, iy = top + 300;
    s.image(IMG, { x: ix, y: iy, h: ih, shadow: false, at: 0.1 });
    s.text('Trước khi nhận:', { font: 'display', size: 46, x: s.cx + 150, y: top + 110, at: 0.3 });
    s.list([
      { text: 'Hạn kiểm định', at: s.time('#apply') + 0.8 },
      { text: 'Tem niêm phong', at: s.time('#apply') + 1.6 },
    ], { x: s.cx - 50, y: top + 220, size: 46, gap: 110, bullet: 'check', bulletColor: 'green' });
    s.box('Đặt gas giao tận nhà', { x: s.cx, y: top + 690, size: 50, w: 640, color: 'accent', at: '#order' });
  },
};
