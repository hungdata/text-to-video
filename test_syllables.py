import subprocess

script = """
## hook

[#h1] Code của bạn là biểu thức hay câu lệnh?

## promise

[#p1] Nhầm lẫn hai khái niệm này là lý do phổ biến gây lỗi cú pháp. [#p2] Trong một phút, bạn sẽ biết biểu thức thực sự là gì.

## concept

[#c1] Biểu thức, hay tiếng Anh là {expression|ếch-x-p-rét-sần}, [#c2] là một đoạn code luôn tính ra được một giá trị duy nhất.

## step1

[#s1_1] Nó có thể chỉ là một con số như số năm.
[#s1_2] Hoặc một phép toán như năm cộng ba.
[#s1_3] Hay thậm chí là một biến số.
[#s1_4] Máy tính sẽ đọc và gom tất cả lại, tính toán để thu về kết quả cuối cùng là tám.

## step2

[#s2_1] Nhưng còn một loại code khác: câu lệnh, hay tiếng Anh là {statement|sờ-tết-mần}.
[#s2_2] Câu lệnh ra lệnh cho máy tính làm một việc gì đó, như tạo ra một biến mới, hoặc kiểm tra điều kiện if else.
[#s2_3] Câu lệnh thực hiện hành động, chứ không trả về một giá trị.
[#s2_4] Đó là lý do bạn không thể gán một lệnh if cho một biến.

## payoff

[#pay1] Tóm lại, biểu thức giống như một danh từ chỉ đồ vật.
[#pay2] Còn câu lệnh là một động từ chỉ hành động. Biểu thức luôn tạo ra giá trị.

## outro

[#o1] Lần tới khi gặp lỗi cú pháp, hãy kiểm tra xem bạn có đặt nhầm một câu lệnh vào chỗ của biểu thức không. Phần tiếp theo: Vòng lặp.
"""

with open("temp_script.md", "w") as f:
    f.write(script)

res = subprocess.run(["python3", ".agents/skills/text-to-video-vi/scripts/syllables.py", "temp_script.md"], capture_output=True, text=True)
print(res.stdout)
