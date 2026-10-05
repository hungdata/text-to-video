# Text-to-Video (Tạo video TikTok tiếng Việt từ văn bản)

Hệ thống tự động tạo video TikTok giải thích kiến thức (explainer) hoặc giới thiệu sản phẩm bán hàng từ chủ đề, tài liệu, bài viết hoặc sách:
- **Định dạng:** Video dọc 9:16 (1080×1920), thời lượng 45–90 giây.
- **Giọng đọc:** Giọng tiếng Việt chuẩn truyền cảm (`vi-VN-NamMinhNeural`).
- **Hình ảnh:** Hiệu ứng vẽ tay (hand-drawn animated whiteboard scenes) bằng Explainroo engine.
- **Phụ đề:** Chữ chạy đồng bộ từng từ (word-synced karaoke captions).

---

## 📁 Cấu trúc dự án

- **`engine/`**: Chứa bản vá tiếng Việt `explainroo-vi.patch` và script cài đặt `setup_cloud.sh`.
- **`tools/`**: Công cụ tạo giọng nói trên macOS (`make_voice_mac.py`) sử dụng Edge-TTS.
- **`prompts/` & `style/`**: Bộ hướng dẫn phong cách (`style_bible.md`), kinh nghiệm (`lessons.md`), và prompt viết kịch bản.
- **`.agents/skills/`**:
  - `text-to-video-vi`: Skill chính điều phối từ kịch bản, vẽ cảnh, sinh giọng đến render video.
  - `batch-video-maker`: Skill sản xuất video hàng loạt theo danh sách chủ đề.
  - `system-monitor`: Giám sát tài nguyên máy Mac khi render.
- **`video_roadmap.md`**: Kế hoạch và danh sách video kiến thức lập trình/công nghệ.

---

## 🚀 Thiết lập & Sử dụng trên macOS

### 1. Kiểm tra môi trường
Chạy script kiểm tra và cài đặt các phụ thuộc (Node.js, ffmpeg, edge-tts):
```bash
bash .agents/skills/text-to-video-vi/scripts/setup_mac.sh
```

### 2. Sử dụng với Antigravity / Agent
Trong Antigravity, kích hoạt kỹ năng `text-to-video-vi` và yêu cầu:
- `"Làm video TikTok giải thích: Thuật toán Dijkstra là gì"`
- `"Tạo video giới thiệu sản phẩm cho đại lý với ảnh này..."`

Agent sẽ tự động nghiên cứu nguồn, viết kịch bản, vẽ hoạt họa, tạo giọng đọc và xuất file video hoàn chỉnh.
