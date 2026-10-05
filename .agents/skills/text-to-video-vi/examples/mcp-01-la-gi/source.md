# Kiểm chứng nguồn — MCP là gì?

Nguồn 1: https://modelcontextprotocol.io/docs/getting-started/intro (đọc 04/10/2026)
Nguồn 2: https://modelcontextprotocol.io/docs/learn/architecture (đọc 04/10/2026)

| Lời đọc | Trích nguồn | Vị trí |
|---|---|---|
| "Đây là một chuẩn mở, dùng để nối ứng dụng AI với các hệ thống bên ngoài." | "MCP (Model Context Protocol) is an open-source standard for connecting AI applications to external systems." | Nguồn 1, ¶1 |
| "Hãy hình dung nó như cổng USB-C. Một kiểu cổng, cắm được đủ loại thiết bị." | "Think of MCP like a USB-C port for AI applications. Just as USB-C provides a standardized way to connect electronic devices, MCP provides a standardized way to connect AI applications to external systems." | Nguồn 1, ¶3 |
| "nối tới dữ liệu, công cụ và quy trình làm việc" | "AI applications like Claude or ChatGPT can connect to data sources (e.g. local files, databases), tools (e.g. search engines, calculators) and workflows (e.g. specialized prompts)" | Nguồn 1, ¶2 |
| "Ứng dụng AI, như Claude, được gọi là host." | "MCP Host: The AI application that coordinates and manages one or multiple MCP clients"; "an MCP host — an AI application like Claude Code or Claude Desktop" | Nguồn 2, Participants |
| "Mỗi nguồn dữ liệu chạy một chương trình nhỏ, gọi là server." | "MCP Server: A program that provides context to MCP clients" | Nguồn 2, Participants |
| "Host mở cho mỗi server một đường nối riêng." | "The MCP host accomplishes this by creating one MCP client for each MCP server. Each MCP client maintains a dedicated connection with its corresponding MCP server." | Nguồn 2, Participants |
| "Công cụ để làm việc, như tra cứu dữ liệu." | "Tools: Executable functions that AI applications can invoke to perform actions (e.g., file operations, API calls, database queries)" | Nguồn 2, Primitives |
| "Tài nguyên để đọc, như nội dung một file." | "Resources: Data sources that provide contextual information to AI applications (e.g., file contents, database records, API responses)" | Nguồn 2, Primitives |
| "những mẫu câu lệnh soạn sẵn" | "Prompts: Reusable templates that help structure interactions with language models" | Nguồn 2, Primitives |
| "AI mở được lịch của bạn là nhờ một server MCP cho lịch" | "Agents can access your Google Calendar and Notion, acting as a more personalized AI assistant." | Nguồn 1, "What can MCP enable?" |

Đơn giản hóa có chủ ý (ghi lại để kiểm tra):
- Lời đọc không nhắc "MCP client" như một thuật ngữ; nói "đường nối riêng" thay cho client. Đúng với nguồn: mỗi client giữ một kết nối riêng tới một server.
- "Tự nó, ứng dụng AI không chạm được vào dữ liệu của bạn" là kiến thức chung (bối cảnh vấn đề), không trình bày như phát hiện của nguồn.
- "Server cho lịch" là ví dụ minh họa; nguồn nêu Google Calendar là việc MCP làm được, không nói một server cụ thể.
