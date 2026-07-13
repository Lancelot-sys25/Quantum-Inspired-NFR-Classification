# Checklist Làm Chủ Bài Trước Khi Nộp

Checklist này tồn tại vì bài báo phải được chính các tác giả bảo vệ được,
không chỉ chạy lại được bằng script. Chưa nên nộp nếu từng tác giả chưa thể tự
giải thích các mục dưới đây mà không nhìn tài liệu.

## Proposition 1: Interference as Label Coupling

- Định nghĩa được `p_l`, `M`, `M'`, và `lambda`.
- Khai triển được `p M'` thành `(1 - lambda) p_l + lambda sum_k p_k M_kl`.
- Giải thích được vì sao các phần tử ngoài đường chéo `M_kl` tạo ra liên kết
  chéo giữa các nhãn.
- Giải thích được vì sao ablation cho thấy interference có tồn tại về mặt
  toán học, nhưng yếu hoặc gây hại trong thiết lập TF-IDF hiện tại.

## Proposition 2: Row-wise Normalization

- Nói rõ `_minmax_rows` làm gì trong `src/quantum_re_nfr/quantum_model.py`.
- Chứng minh được vì sao row-wise min-max normalization giữ nguyên thứ hạng
  các nhãn trong cùng một instance.
- Giải thích được vì sao một global threshold sau row-wise normalization trở
  thành threshold raw-score phụ thuộc vào từng instance.
- Tự đưa được ví dụ hai nhãn:
  - `u = (0.5, 0.0)` dự đoán nhãn 1 sau normalization;
  - `u = (0.5, 0.9)` có cùng raw score cho nhãn 1 nhưng không dự đoán nhãn 1.
- Giải thích được vì sao điều này nghĩa là decision rule đang triển khai không
  chỉ là threshold centroid độc lập cho từng nhãn.

## Phân Tích Thống Kê

- Giải thích được Micro-F1, Macro-F1, Hamming loss, và LRAP.
- Giải thích được vì sao Wilcoxon trên 5 fold có độ phân giải rất thấp, và vì
  sao `p=0.0625` là giá trị hai phía khác 0 nhỏ nhất có thể đạt được khi
  `n=5`.
- Giải thích được paired Cohen's `d_z`: trung bình chênh lệch theo cặp chia
  cho độ lệch chuẩn của các chênh lệch theo cặp.
- Giải thích được vì sao bootstrap interval trên held-out requirements là hữu
  ích, nhưng không thay thế được một dataset độc lập thứ hai.
- Giải thích được vì sao hiệu ứng khoảng `d_z = 0.5` cần xấp xỉ 30-35 paired
  folds để có statistical power thông thường, và vì sao dataset hiện tại không
  thể cung cấp điều đó một cách trung thực.

## ERASER Sufficiency

- Định nghĩa được comprehensiveness là độ giảm score sau khi xóa các rationale
  tokens.
- Định nghĩa được sufficiency là `f(x)_c - f(x_top-k)_c`.
- Nói rõ sufficiency càng thấp càng tốt.
- Giải thích được vì sao sufficiency âm là bất thường nhưng vẫn có thể xảy ra:
  input chỉ gồm rationale nhận score cao hơn input đầy đủ.
- Giải thích được vì sao bài diễn giải sufficiency âm một cách thận trọng như
  khả năng lọc background noise, không xem đó là bằng chứng rằng explanation
  hữu ích với con người.

## Định Vị Đóng Góp

- Nói được đóng góp dương của bài trong một câu:
  một bộ phân loại NFR đa nhãn quantum-inspired có giải thích nội tại, cộng
  với phân tích lý thuyết và thực nghiệm chỉ ra khi nào hình học của nó giúp
  ích và khi nào không.
- Nói rõ bài không claim điều gì:
  không claim state-of-the-art accuracy, và không claim accuracy gain đã có ý
  nghĩa thống kê so với classical baselines.
- Giải thích được vì sao bài vẫn có thể công bố:
  reviewer có thể đánh giá cao một scoring framework minh bạch, intrinsic
  explanations, và một kết quả diagnostic/negative trung thực nếu claim được
  đặt đúng phạm vi.

## Làm Chủ Tính Tái Lập

- Biết script nào sinh ra từng bảng kết quả chính.
- Biết số DistilBERT được lưu ở đâu.
- Biết vì sao anonymous artifact không được chứa local paths, tên tác giả, tên
  trường/đơn vị, email, hoặc link GitHub gốc.
