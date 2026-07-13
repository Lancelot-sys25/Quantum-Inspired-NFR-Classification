# Trả Lời Nhận Xét Bài Báo NFR FISAT 2026

Tài liệu này trả lời trực tiếp từng mục trong file
`NHAN_XET_BAI_NFR_FISAT_2026.md`. Các số liệu bên dưới lấy từ các file kết quả
đã xuất trong thư mục `reports/`; không có số liệu nào được suy đoán bằng tay.

---

## A. Các Vấn Đề Khoa Học

### A1. Interference: có giúp thật không?

Đã chạy lại ablation interference cho cả positive projection và contrastive
projection bằng `scripts/run_nice_ablation_experiment.py`. Kết quả nằm trong
`reports/nice_ablation_summary.csv` và
`reports/quantum_contribution_effect_sizes.csv`.

| Biến thể | Macro-F1 mean ± std |
|---|---:|
| Positive projection, không interference | 0.5526 ± 0.0285 |
| Positive projection, có interference | 0.5490 ± 0.0237 |
| Contrastive projection, không interference | 0.5397 ± 0.0398 |
| Contrastive projection, có interference | 0.4118 ± 0.0275 |

Hiệu ứng interference:

| So sánh | Δ Macro-F1 | Cohen's dz | Wilcoxon p |
|---|---:|---:|---:|
| Positive: có interference - không interference | -0.0037 | -0.21 | 0.8125 |
| Contrastive: có interference - không interference | -0.1279 | -2.89 | 0.0625 |

Kết luận: interference không phải đóng góp accuracy đáng tin cậy. Với positive
projection, hiệu ứng gần như bằng 0. Với contrastive projection, interference
làm giảm mạnh Macro-F1. Vì vậy bài đã hạ interference xuống đúng vai trò: một
cơ chế coupling có ý nghĩa lý thuyết để phân tích decision rule, không được
trình bày như nguồn cải thiện accuracy chính.

Các chỗ đã sửa trong `paper/main.tex`:

- phần contribution không còn tôn vinh interference như đóng góp accuracy;
- phần Theoretical Characterization mô tả interference là một nguồn cross-label
  coupling;
- phần Ablation Study nói rõ interference là thành phần thứ cấp, phần lớn không
  hoạt động hiệu quả trong thiết lập TF-IDF hiện tại.

### A2. Đóng góp quantum có thật không, hay hybrid chỉ là SVM?

Đã định lượng riêng phần đóng góp quantum bằng so sánh hybrid với SVM-only dùng
cùng backbone TF-IDF sublinear. Kết quả nằm trong
`reports/quantum_contribution_effect_sizes.csv` và
`reports/nice_paired_bootstrap_summary.csv`.

| So sánh | Δ Macro-F1 | Cohen's dz | Wilcoxon p |
|---|---:|---:|---:|
| Hybrid vs TF-IDF Linear SVM | +0.0035 | 0.73 | 0.1875 |
| Hybrid vs TF-IDF Logistic Regression | +0.0107 | 0.54 | 0.4375 |
| Hybrid vs Sentence-BERT | -0.0037 | -0.19 | 0.8125 |
| Hybrid vs SVM-only cùng backbone | +0.0140 | 0.49 | 0.3125 |
| Pure contrastive projection vs TF-IDF Linear SVM | -0.1931 | -5.92 | 0.0625 |
| Pure positive projection vs TF-IDF Linear SVM | -0.0559 | -1.36 | 0.0625 |

Bootstrap trên held-out requirements:

| So sánh | Δ Macro-F1 | 95% CI | p bootstrap |
|---|---:|---:|---:|
| Hybrid vs TF-IDF Linear SVM | +0.0081 | [-0.0100, 0.0263] | 0.376 |
| Hybrid vs TF-IDF Logistic Regression | +0.0020 | [-0.0205, 0.0227] | 0.918 |
| Hybrid vs pure contrastive projection | +0.1401 | [0.0741, 0.2127] | 0.000 |

Kết luận: phần quantum thuần không cạnh tranh được với SVM. Hybrid có tăng
nhẹ so với SVM-only cùng backbone (+0.0140 Macro-F1), nhưng chưa có ý nghĩa
thống kê và bootstrap interval của các so sánh chính đều vắt qua 0. Vì vậy bài
đã được tái định vị quanh interpretability và diagnostic analysis, không claim
state-of-the-art accuracy.

Các chỗ đã sửa trong `paper/main.tex`:

- Abstract nói đóng góp chính là intrinsic explanation và characterization,
  không phải accuracy SOTA;
- Discussion nêu rõ hybrid gain là suggestive, not confirmed;
- Conclusion đặt đóng góp ở transparent multi-label scoring framework và phân
  tích khi nào geometry giúp/không giúp.

### A3. Chỉ có một dataset nhỏ: xử lý thế nào?

Chọn hướng thêm baseline transformer fine-tuned thay vì thêm dataset thứ hai,
vì hiện không có sẵn dataset NFR multi-label công khai khác đủ tương thích để
kiểm chứng interference/co-occurrence. Baseline được thêm bằng
`scripts/run_nice_finetuned_transformer_experiment.py`.

Thông số DistilBERT:

- model: `distilbert-base-uncased`;
- 5-fold CV;
- 2 epochs;
- batch size 16;
- max length 128;
- learning rate `5e-5`;
- BCE loss với clipped positive class weights;
- per-label threshold calibration.

Kết quả trong
`reports/nice_finetuned_transformer_distilbert_base_uncased_summary.csv`:

| Model | Micro-F1 | Macro-F1 | Hamming loss | LRAP |
|---|---:|---:|---:|---:|
| Fine-tuned DistilBERT | 0.5420 ± 0.0569 | 0.5333 ± 0.0591 | 0.1402 ± 0.0361 | 0.7105 ± 0.0516 |

Kết luận: trên dataset nhỏ và mất cân bằng này, fine-tuned DistilBERT yếu hơn
Sentence-BERT+LR, TF-IDF baselines, và hybrid model. Điều này giúp bài không
chỉ dựa vào SBERT đông cứng khi so với neural baseline. Tuy nhiên, bài vẫn ghi
rõ limitation: một dataset 381 mẫu không đủ để claim ranking tổng quát cho mọi
NFR corpus.

Các chỗ đã sửa trong `paper/main.tex`:

- DistilBERT được thêm vào Compared Models và Hyperparameters;
- DistilBERT là một dòng trực tiếp trong bảng kết quả CV chính;
- Threats to Validity ghi rõ hạn chế một dataset nhỏ và baseline scope.

### A4. Hai Proposition có khớp với mô hình thật không?

Đã kiểm lại với code trong `src/quantum_re_nfr/quantum_model.py`. Điểm quan
trọng là implementation luôn dùng row-wise min-max normalization trước khi
thresholding. Vì vậy phát biểu cũ kiểu "threshold tương đương cosine cutoff cố
định" là chưa khớp với cách mô hình ra quyết định.

Bài đã sửa phần Theoretical Characterization thành hai ý:

1. Interference tạo coupling qua ma trận đồng xuất hiện label.
2. Row-wise normalization giữ nguyên ranking trong cùng instance, nhưng biến
   global threshold thành raw-score threshold phụ thuộc vào instance.

Ý nghĩa của Proposition về normalization:

- ranking giữa các label trong cùng một requirement được giữ nguyên;
- tại `lambda = 0`, ranking này tương ứng với ranking theo cosine/projection;
- nhưng decision nhị phân sau threshold không tương đương với L classifier độc
  lập có cùng cutoff cố định;
- hai instance có cùng raw score cho một label vẫn có thể nhận quyết định khác
  nhau nếu score của các label còn lại khác nhau.

Tài liệu hỗ trợ vấn đáp đã được thêm tại
`docs/author_mastery_checklist.md` và bản Word
`docs/author_mastery_checklist_vi.docx`. Tuy nhiên đây chỉ là checklist học:
từng tác giả vẫn phải tự hiểu và tự bảo vệ được mệnh đề.

### A5. Explainability có đủ sâu không?

Đã bổ sung ERASER-style comprehensiveness và sufficiency, kèm random control
và baseline TF-IDF Linear SVM dùng coefficient-based explanation. Kết quả nằm
trong `reports/nice_deletion_comparison_summary.csv`.

| Explainer | Comprehensiveness | Random comp. | Sufficiency | Random suff. | Ratio comp. | Ratio suff. |
|---|---:|---:|---:|---:|---:|---:|
| Contrastive projection intrinsic | 0.0305 | 0.0059 | -0.0395 | 0.0337 | 5.21x | -1.17x |
| TF-IDF Linear SVM coefficients | 0.0867 | 0.0216 | 0.0484 | 0.1141 | 4.01x | 0.42x |

Quy ước sufficiency đã được ghi rõ trong bài:

`Sufficiency = f(x)_c - f(x_top-k)_c`.

Sufficiency càng thấp càng tốt. Giá trị âm nghĩa là input chỉ gồm top-k
rationale nhận score cao hơn input đầy đủ. Bài diễn giải điều này thận trọng:
có thể do non-rationale tokens tạo background noise, nhưng không được xem là
bằng chứng rằng explanation hữu ích với con người.

Kết luận: phần "Explainable" trong tiêu đề hiện được hỗ trợ bởi intrinsic
token-level contribution và deletion-based faithfulness theo ERASER-style
metrics. Claim vẫn được giới hạn ở model faithfulness, không claim human
usefulness.

---

## B. Tự Kiểm Tuân Thủ Hội Nghị

### B1. Ẩn danh double-blind

Đã kiểm PDF và source review:

- `paper/main.tex` dùng `Anonymous Author(s)`;
- affiliation là `Affiliation withheld for double-blind review`;
- không dùng bản camera-ready có tên tác giả cho review;
- source zip review chỉ chứa `main.tex`, `llncs.cls`, `splncs04.bst`,
  `references.bib`.

Scan package nộp mới không thấy tên tác giả, email, đường dẫn máy cá nhân,
link GitHub gốc, hoặc file camera-ready có tên tác giả.

### B2. Artifact ẩn danh

Artifact được dựng lại bằng `scripts/make_review_artifact.ps1`:

`artifacts/nfr_eai_fisat_2026_review_artifact.zip`

Đã giải nén và scan các chuỗi nhạy cảm:

- tên tác giả;
- email;
- tên tài khoản GitHub gốc;
- link repo gốc;
- local paths;
- file camera-ready có tên tác giả.

Kết quả scan package mới: không có match. Link anonymous cũng đã kiểm HTTP và
trả `200 OK`:

`https://anonymous.4open.science/r/nfr-review-artifact-CE2D/`

Việc còn lại trước khi bấm nộp: nhóm phải tự mở link này bằng incognito browser
và soi README, file tree, commit/history hiển thị trên anonymous mirror.

### B3. Khai báo AI

Đã sửa `Use of AI Tools` trong `paper/main.tex` để mô tả AI là công cụ hỗ trợ:

- implementation checks;
- dependency diagnosis;
- experiment re-runs;
- statistical-script review;
- consistency checks;
- language editing.

Câu khai hiện không nói rằng AI là tác giả của proposition, statistical
interpretation, contribution framing, hoặc final claims. Bài ghi rõ các tác
giả đã independently reviewed and rewrote các phần đó và chịu trách nhiệm cuối
cùng. Điều kiện bắt buộc vẫn là từng tác giả phải thật sự hiểu và bảo vệ được
các phần này.

### B4. Nộp đúng file

File review cần nộp:

- PDF anonymous: `paper/main.pdf`;
- source anonymous: `source_anonymous_lncs.zip` trong package submission;
- artifact anonymous: `nfr_eai_fisat_2026_review_artifact.zip`.

Không nộp bản camera-ready vì file đó có tên tác giả và chỉ dùng sau khi
accepted.

### B5. Trang và track

Đã build bản cuối bằng `lmodern` + `microtype`.

Kết quả:

- `paper/main.pdf`: 15 trang tổng;
- body đến `Conclusion`: tối đa 14 trang;
- references và disclosure nằm ở cuối trang 14 và trang 15.

Như vậy body nằm trong giới hạn 12-15 trang của full paper, và tổng PDF cũng
không vượt 15 trang.

Track và Scope trên Confy+ là thao tác web form, nhóm phải tự chọn đúng khi
nộp vì repo không lưu trạng thái đó.

---

## C. Camera-ready

Chưa xử lý camera-ready vì đây là việc sau khi accepted, đúng như feedback của
thầy. Các việc cần nhớ:

- lưu file camera-ready bằng UTF-8 không BOM;
- thay link anonymous bằng repo thật hoặc DOI Zenodo;
- thêm ORCID;
- rà Acknowledgements.

---

## File Giao Lại

- `.tex` đã sửa: `paper/main.tex`
- PDF đã build: `paper/main.pdf`
- Artifact: `artifacts/nfr_eai_fisat_2026_review_artifact.zip`
- Package nộp mới nhất: `submission/fisat2026_review_20260713_222340`
- Checklist vấn đáp: `docs/author_mastery_checklist.md`
- Checklist Word tiếng Việt: `docs/author_mastery_checklist_vi.docx`
