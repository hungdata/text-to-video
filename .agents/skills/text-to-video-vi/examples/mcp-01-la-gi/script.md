# MCP là gì?

> Series: Công nghệ · Hiểu nhanh AI · Phần 1
> Nguồn: modelcontextprotocol.io, "What is the Model Context Protocol (MCP)?" và "Architecture overview" (đọc 04/10/2026)
> Hook đã chọn: A (Câu hỏi có hệ quả) — chạm điều người dùng AI đã thấy tận mắt, dẫn thẳng vào câu trả lời ở payoff.
> Hook A (Câu hỏi có hệ quả): lời "Vì sao AI giờ mở được lịch của bạn?" | chữ "AI mở lịch của bạn?" | hình: robot đi tới, cuốn lịch bật mở
> Hook B (Ngược đời): lời "AI rất giỏi, nhưng tự nó không mở nổi một file." | chữ "Giỏi mà không mở được file" | hình: file bị khóa rung lắc
> Hook C (Khoảng trống tò mò): lời "Có một cái cổng nhỏ nối AI với mọi thứ." | chữ "Một cổng cho AI" | hình: phích cắm lao vào ổ

## hook {hold=0.4}
[#q] Vì sao {AI|ây ai} giờ mở được [#cal] lịch của bạn?
> [#q] tiêu đề "AI mở *lịch* của bạn?" enter none; robot (bot) trượt vào; [#cal] icon lịch bật ra, mũi tên robot → lịch

## promise
[#alone] Tự nó, ứng dụng {AI|ây ai} không chạm được vào dữ liệu của bạn. [#promise] Trong một phút, bạn sẽ biết thứ gì nối nó với bên ngoài.
> [#alone] robot trong khung nét đứt, file và lịch ở ngoài bị gạch; [#promise] dấu hỏi giữa robot và thế giới

## concept {hold=0.8}
[#term] Thứ đó tên là {MCP|em xi pi}. [#std] Đây là một chuẩn mở, dùng để nối ứng dụng {AI|ây ai} với các hệ thống bên ngoài.
> [#term] chữ MCP to, màu nhấn; [#std] dòng nhỏ "Model Context Protocol · chuẩn mở"

## step1
[#usb] Hãy hình dung nó như cổng {USB-C|u ét bê xê}. [#plug] Một kiểu cổng, cắm được đủ loại thiết bị. [#three] Với {AI|ây ai}, cái cổng này nối tới dữ liệu, công cụ và quy trình làm việc. [#deeper] Nhưng bên trong nó chạy thế nào?
> [#usb] icon usb giữa màn; [#plug] 3 thiết bị quanh cổng; [#three] đổi nhãn: Dữ liệu / Công cụ / Quy trình; [#deeper] dấu hỏi nhỏ

## step2
[#host] Ứng dụng {AI|ây ai}, như Claude, được gọi là host. [#server] Mỗi nguồn dữ liệu chạy một chương trình nhỏ, gọi là server. [#client] Host mở cho mỗi server một đường nối riêng.
> [#host] hộp "Host · Claude" trên cùng; [#server] 2 hộp server: Lịch, File; [#client] 2 mũi tên riêng host → từng server

## step3
[#offer] Mỗi server đưa cho {AI|ây ai} ba thứ. [#tools] Công cụ để làm việc, như tra cứu dữ liệu. [#res] Tài nguyên để đọc, như nội dung một file. [#prompts] Và những mẫu câu lệnh soạn sẵn.
> [#offer] hộp server; [#tools] wrench "Công cụ"; [#res] file-text "Tài nguyên"; [#prompts] message-square "Mẫu lệnh"

## payoff {hold=1.2}
[#answer] Vậy {AI|ây ai} mở được lịch của bạn là nhờ một server {MCP|em xi pi} cho lịch, [#plugged] cắm vào ứng dụng qua chuẩn chung này.
> [#answer] lại sơ đồ host → server Lịch, tô màu nhấn đường nối; [#plugged] icon lịch sáng lên

## outro {hold=1.6}
[#apply] Lần tới thấy chữ {MCP|em xi pi} trong một ứng dụng, bạn biết đó là cái cổng cắm cho {AI|ây ai}. [#next] Bạn muốn xem cách cắm server đầu tiên không?
> [#apply] chữ "MCP = cổng cắm cho AI"; [#next] dòng "Phần 2: cắm server đầu tiên?"

> ---
> Âm tiết: (đếm bằng máy sau khi chạy voice)
> Chấm: Hook 4 (câu hỏi rõ, chạm trải nghiệm thật; chưa có yếu tố bất ngờ mạnh) · Lời hứa 5 · Một ý 5 · Dễ hiểu 4 (host/server là từ tiếng Anh, đã giải thích bằng vai trò) · Chính xác 5 · Hình 5 · Đóng vòng 5 · Độ dài 5
> Tóm một câu: MCP là chuẩn mở, như cổng USB-C, để ứng dụng AI cắm vào dữ liệu và công cụ bên ngoài qua các server.
