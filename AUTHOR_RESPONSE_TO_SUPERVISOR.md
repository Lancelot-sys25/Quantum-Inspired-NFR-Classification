# Trả lời nhận xét bản NFR FISAT 2026

Ngày kiểm tra: 2026-07-21

## 1. Giới hạn trang

Bản anonymous đã được build lại với LNCS, `lmodern` và `microtype`:

- PDF có đúng 15 trang;
- `Conclusion` bắt đầu ở trang 13;
- `Reproducibility`, LNCS credits và References bắt đầu ở trang 14;
- References kết thúc ở trang 15;
- không có overfull box, citation hoặc reference chưa định nghĩa.

Phần Results, Discussion và Threats đã được rút gọn bằng cách bỏ nội dung lặp;
không giảm cỡ chữ và không bỏ số liệu hoặc giới hạn nghiên cứu.

## 2. Đóng góp và bằng chứng

Bài được định vị là đóng góp về khả năng giải thích nội tại và phân tích hình
học chẩn đoán, không tuyên bố state-of-the-art. Sentence-BERT vẫn là baseline
mạnh nhất về Macro-F1/LRAP. Hybrid quantum--SVM cạnh tranh với TF-IDF nhưng
không có lợi thế accuracy được xác nhận thống kê.

Proposition 1 mô tả interference; Proposition 2 (`prop:reduction`) xác định
điều kiện quy giản và trường hợp row-wise normalization tạo cross-label
coupling. Các phát biểu này khớp với implementation và ablation đã xuất.

## 3. Explainability

ERASER-style comprehensiveness và sufficiency được so với random deletion và
SVM coefficient baseline. Claim chỉ giới hạn ở model faithfulness, không suy
rộng thành chất lượng rationale đối với con người.

## 4. AI và quyền làm chủ

Khai báo AI nằm trong môi trường `credits` chuẩn LNCS, dưới
`\subsubsection{\ackname}`. Tác giả phải tự giải thích được propositions,
Wilcoxon, bootstrap, effect size, power analysis và sufficiency trước khi nộp.

## 5. Artifact và file nộp

- Source anonymous: `artifacts/fisat_2026_overleaf_anonymous_source_audited.zip`
- PDF anonymous: `output/pdf/fisat_2026_anonymous_submission_audited.pdf`
- Artifact công khai: <https://anonymous.4open.science/r/nfr-review-artifact-CE2D/>

Không upload `paper/main_cameraready.tex` trong giai đoạn double-blind.
