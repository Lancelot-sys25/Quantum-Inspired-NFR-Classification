# Đề Cương Nghiên Cứu

## Tên đề tài

**Explainable Quantum-Inspired Multi-label Classification of Non-Functional Requirements**

Tên tiếng Việt: **Phân loại đa nhãn yêu cầu phi chức năng bằng mô hình quantum-inspired có khả năng giải thích**

## Bối cảnh

Trong Requirements Engineering, nhiều yêu cầu phi chức năng không thuộc một nhãn duy nhất. Một yêu cầu về mã hóa dữ liệu có thể liên quan đến security, reliability và compliance. Một yêu cầu về thời gian phản hồi có thể vừa là performance vừa ảnh hưởng usability. Cách phân loại cứng một nhãn thường làm mất thông tin về sự chồng chéo này.

Mô hình quantum-inspired phù hợp với bài toán vì có thể biểu diễn requirement như một trạng thái ngữ nghĩa phân bố qua nhiều lớp, thay vì buộc requirement chỉ thuộc một lớp duy nhất.

## Vấn đề nghiên cứu

Các mô hình phân loại yêu cầu hiện nay thường mạnh về dự đoán nhãn, nhưng còn hạn chế ở ba điểm:

- Chưa mô hình hóa rõ sự chồng chéo giữa các loại NFR.
- Khó giải thích vì sao một requirement thuộc nhiều nhãn cùng lúc.
- Dễ nhầm giữa các lớp NFR có từ vựng gần nhau, ví dụ reliability, availability và performance.

## Mục tiêu

1. Xây dựng mô hình quantum-inspired cho phân loại đa nhãn NFR.
2. So sánh mô hình với baseline truyền thống và mô hình transformer.
3. Đề xuất cơ chế giải thích theo semantic amplitude cho từng nhãn.
4. Đánh giá độ ổn định của mô hình trên nhiều dataset công khai.

## Phương pháp đề xuất

Mỗi requirement được chuyển thành vector đặc trưng ngữ nghĩa. Vector này được chuẩn hóa thành một trạng thái semantic state. Mỗi nhãn NFR được xem như một trục hoặc một projection trong không gian ngữ nghĩa. Xác suất thuộc nhãn được tính từ biên độ chiếu của requirement lên từng nhãn.

Mô hình có thể bổ sung thành phần interference để điều chỉnh trường hợp các nhãn hỗ trợ hoặc triệt tiêu nhau. Ví dụ, các tín hiệu "encrypt", "access control" và "authentication" khuếch đại nhãn security; trong khi các tín hiệu "response time", "throughput" và "latency" khuếch đại nhãn performance.

## Câu hỏi nghiên cứu

- RQ1: Mô hình quantum-inspired có cải thiện Micro-F1 và Macro-F1 không?
- RQ2: Mô hình có xử lý tốt hơn các requirement đa nhãn so với baseline không?
- RQ3: Giải thích theo semantic amplitude có giúp nhận diện từ/cụm từ quan trọng cho từng nhãn không?

## Đóng góp kỳ vọng

- Một mô hình quantum-inspired chạy trên PC thường, không yêu cầu phần cứng lượng tử.
- Một pipeline thực nghiệm tái lập được cho NFR multi-label classification.
- Một cơ chế giải thích gọn, dễ trình bày trong paper.
- Kết quả benchmark với PROMISE/NICE và baseline phổ biến.

## Rủi ro

- Dataset có thể không đồng nhất về taxonomy nhãn.
- Một số dataset chỉ hỗ trợ single-label, cần chuyển đổi hoặc chọn subset phù hợp.
- Cần mô tả mô hình bằng công thức rõ để tránh bị hiểu là dùng quantum như ẩn dụ.

## Hướng nộp bài

Hội nghị mục tiêu: **EAI FISAT 2026, Ho Chi Minh City, 25-27/11/2026**.

