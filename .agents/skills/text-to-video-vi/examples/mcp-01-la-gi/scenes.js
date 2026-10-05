// MCP là gì? — Hiểu nhanh AI, Phần 1. Vùng an toàn TikTok: 745×746 tại (119, 304).
export default {
  hook(s) {
    const top = s.safe.y;
    s.text('AI mở *lịch*\ncủa bạn?', { font: 'display', size: 92, y: top + 120, enter: 'none', at: 0 });
    s.icon('bot', { id: 'bot', x: s.safe.left + 170, y: top + 470, size: 170, color: 'blue', enter: 'slide-right', at: 0, float: 6 });
    s.icon('calendar', { id: 'cal', x: s.safe.right - 170, y: top + 470, size: 170, color: 'accent', enter: 'pop', at: '#cal' });
    s.arrow('bot', 'cal', { at: s.time('#cal') + 0.15, bend: -0.3 });
  },

  promise(s) {
    const top = s.safe.y;
    s.box('', { id: 'cage', x: s.cx, y: top + 230, w: 300, h: 260, dashed: true, color: 'gray', at: '#alone' });
    s.icon('bot', { x: s.cx, y: top + 230, size: 150, color: 'blue', at: -1 });
    s.icon('calendar', { id: 'c2', x: s.safe.left + 120, y: top + 560, size: 110, color: 'muted', at: s.time('#alone') + 0.5 });
    s.icon('file-text', { id: 'f2', x: s.safe.right - 120, y: top + 560, size: 110, color: 'muted', at: s.time('#alone') + 0.8 });
    s.annotate('c2', { type: 'cross', color: 'red', at: s.time('#alone') + 1.3 });
    s.annotate('f2', { type: 'cross', color: 'red', at: s.time('#alone') + 1.5 });
    s.text('?', { font: 'display', size: 160, x: s.cx, y: top + 580, color: 'accent', at: '#promise', enter: 'pop' });
  },

  concept(s) {
    const top = s.safe.y;
    s.text('*MCP*', { id: 'mcp', font: 'display', size: 190, y: top + 240, at: '#term', enter: 'pop' });
    s.text('Model Context Protocol', { size: 46, y: top + 430, color: 'muted', at: '#std' });
    s.box('chuẩn mở', { x: s.cx, y: top + 560, size: 54, icon: 'unlock', color: 'green', at: s.time('#std') + 0.6 });
  },

  step1(s) {
    const top = s.safe.y;
    const cy = top + 360;
    s.icon('usb', { id: 'usb', x: s.cx, y: cy, size: 180, color: 'accent', at: '#usb', bg: 'circle' });
    const spots = [
      { x: s.cx, y: top + 90 },
      { x: s.safe.left + 110, y: top + 600 },
      { x: s.safe.right - 110, y: top + 600 },
    ];
    const devices = ['laptop', 'smartphone', 'headphones'];
    const kinds = [
      { icon: 'database', label: 'Dữ liệu', color: 'blue' },
      { icon: 'wrench', label: 'Công cụ', color: 'purple' },
      { icon: 'workflow', label: 'Quy trình', color: 'green' },
    ];
    const tThree = s.time('#three');
    spots.forEach((p, i) => {
      const id = `dev${i}`;
      s.icon(devices[i], { id, x: p.x, y: p.y, size: 100, color: 'muted', at: s.time('#plug') + i * 0.3, out: tThree - 0.1 });
      s.icon(kinds[i].icon, { id: `k${i}`, x: p.x, y: p.y, size: 100, color: kinds[i].color, label: kinds[i].label, labelSize: 44, at: tThree + i * 0.5 });
      s.arrow('usb', [p.x, p.y + (i === 0 ? 70 : -70)], { at: s.time('#plug') + i * 0.3 + 0.2, head: 'none', dashed: true });
    });
    s.text('?', { font: 'display', size: 110, x: s.safe.right - 60, y: top + 120, color: 'accent', at: '#deeper', enter: 'pop' });
  },

  step2(s) {
    const top = s.safe.y;
    s.box('Host · Claude', { id: 'host', x: s.cx, y: top + 120, size: 56, icon: 'bot', color: 'blue', at: '#host' });
    s.box('Lịch', { id: 'sv1', x: s.safe.left + 170, y: top + 560, size: 52, icon: 'calendar', color: 'accent', at: '#server' });
    s.box('File', { id: 'sv2', x: s.safe.right - 170, y: top + 560, size: 52, icon: 'folder', color: 'teal', at: s.time('#server') + 0.4 });
    s.note('server', { x: s.cx, y: top + 680, size: 40, at: s.time('#server') + 0.8 });
    s.arrow('host', 'sv1', { at: '#client', label: 'đường riêng', labelSize: 36 });
    s.arrow('host', 'sv2', { at: s.time('#client') + 0.5 });
  },

  step3(s) {
    const top = s.safe.y;
    s.box('Server', { id: 'srv', x: s.cx, y: top + 90, size: 56, icon: 'server', color: 'teal', at: '#offer' });
    s.list([
      { text: 'Công cụ', icon: 'wrench', color: 'purple', at: '#tools' },
      { text: 'Tài nguyên', icon: 'file-text', color: 'blue', at: '#res' },
      { text: 'Mẫu lệnh', icon: 'message-square', color: 'green', at: '#prompts' },
    ], { x: s.safe.left + 150, y: top + 260, size: 64, gap: 130 });
  },

  payoff(s) {
    const top = s.safe.y;
    s.box('Host · Claude', { id: 'h', x: s.cx, y: top + 110, size: 56, icon: 'bot', color: 'blue', at: '#answer' });
    s.box('Server MCP · Lịch', { id: 's', x: s.cx, y: top + 470, size: 52, icon: 'calendar', color: 'accent', at: s.time('#answer') + 0.4 });
    s.arrow('h', 's', { at: '#plugged', color: 'accent', width: 6, label: 'MCP', labelSize: 44 });
    s.annotate('s', { type: 'circle', color: 'accent', at: s.time('#plugged') + 0.6 });
  },

  outro(s) {
    const top = s.safe.y;
    s.text('*MCP* = cổng cắm\ncho AI', { id: 'sum', font: 'display', size: 84, y: top + 200, at: '#apply' });
    s.icon('plug', { x: s.cx, y: top + 420, size: 130, color: 'accent', at: s.time('#apply') + 0.5 });
    s.box('Phần 2: cắm server đầu tiên?', { x: s.cx, y: top + 620, size: 44, color: 'gray', dashed: true, at: '#next' });
  },
};
