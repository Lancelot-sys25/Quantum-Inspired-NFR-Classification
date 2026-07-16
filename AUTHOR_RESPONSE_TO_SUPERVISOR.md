# Trả Lời Nhận Xét Bản Mới NFR FISAT 2026

Tài liệu này trả lời trực tiếp file
`NHAN_XET_BAI_NFR_FISAT_2026_v2.md`. Bản sửa tương ứng nằm ở
`paper/main.tex`; PDF build cuối là `paper/main.pdf`.

---

## 1. Giới hạn trang

Đã build lại bản cuối với `lmodern` và `microtype`.

Kết quả đo trên PDF thật:

- `paper/main.pdf`: 15 trang tổng;
- phần body đến `Conclusion`: tối đa 14 trang;
- `Conclusion`, `Reproducibility`, `Use of AI Tools`, và phần đầu
  `References` nằm ở trang 14;
- references kết thúc ở trang 15.

Như vậy body không vượt 15 trang, và tổng PDF cũng đã giảm từ 16 xuống 15
trang.

Các phần đã nén:

- nén đoạn `Dataset size and availability` trong Threats;
- rút gọn proof/remark của Proposition về row-wise normalization;
- bỏ các câu lặp caveat trong Discussion;
- gộp đoạn DistilBERT riêng vào phần giải thích bảng kết quả;
- nén `Related Work`, `Future Work`, `Reproducibility`, và `Use of AI Tools`.

## 2. Cân lại đóng góp dương của bài

Đã viết lại abstract, introduction/contribution list, discussion framing, và
conclusion để đặt đóng góp dương lên trước.

Thông điệp chính hiện tại:

- bài đề xuất một phương pháp phân loại NFR đa nhãn có giải thích nội tại;
- token-level semantic amplitude contributions được lấy trực tiếp từ scoring
  function, không cần post-hoc explainer;
- phần lý thuyết chỉ rõ khi nào geometry tương đương cosine-style ranking và
  khi nào interference hoặc row-wise normalization tạo cross-label coupling;
- ablation cho biết thành phần nào giúp, thành phần nào yếu hoặc không nên
  thổi phồng.

Giới hạn vẫn được giữ trung thực: bài không claim state-of-the-art accuracy và
không claim hybrid gain đã có ý nghĩa thống kê. Tuy nhiên, bài hiện được định
vị như một đóng góp về intrinsic interpretability + diagnostic theory cho
multi-label NFR classification, thay vì như một lời xin lỗi vì không thắng mọi
baseline.

Lý do đóng góp này vẫn đủ sức thuyết phục reviewer:

- yêu cầu NFR đa nhãn cần cả dự đoán lẫn khả năng giải thích;
- nhiều baseline mạnh hơn về embedding/accuracy nhưng cần post-hoc explanation;
- bài cung cấp scoring framework minh bạch, giải thích trực tiếp theo token,
  và kiểm tra faithfulness bằng ERASER-style metrics;
- kết quả âm/không đáng kể về accuracy được biến thành diagnostic insight rõ
  ràng, không bị che giấu.

## 3. DistilBERT trong bảng kết quả

Sau khi truy vết metadata, dòng fine-tuned DistilBERT chỉ được giữ trong bảng
per-label threshold. Dòng này đã bị loại khỏi bảng global-threshold vì không có
thí nghiệm DistilBERT theo protocol global-threshold.

Số liệu lấy từ
`reports/nice_finetuned_transformer_distilbert_base_uncased_summary.csv`:

| Model | Micro-F1 | Macro-F1 | Hamming loss | LRAP |
|---|---:|---:|---:|---:|
| Fine-tuned DistilBERT | 0.5420 ± 0.0569 | 0.5333 ± 0.0591 | 0.1402 ± 0.0361 | 0.7105 ± 0.0516 |

Không thêm dòng single-split hoặc global-threshold cho DistilBERT vì thí nghiệm
DistilBERT hiện chỉ được chạy theo protocol 5-fold CV với per-label calibration.
Bài không tái sử dụng hoặc ước lượng số cho protocol chưa chạy.

## 4. Khai báo AI và quyền làm chủ của tác giả

Đã sửa `Use of AI Tools` để phản ánh AI ở vai trò hỗ trợ:

- implementation checks;
- dependency diagnosis;
- experiment re-runs;
- statistical-script review;
- consistency checks;
- language editing.

Bản khai hiện không còn viết theo hướng AI "tính toàn bộ", "suy ra chứng minh",
hay "định hình lõi đóng góp" như thể AI là người làm phần trí tuệ chính. Đồng
thời, cách xử lý không phải là giấu vai trò AI: bài vẫn ghi rõ có dùng AI hỗ
trợ, và tác giả chịu trách nhiệm cuối cùng.

Điều kiện bắt buộc trước khi nộp:

- từng tác giả phải tự suy lại hai Proposition và giải thích được từng bước;
- từng tác giả phải hiểu effect size, bootstrap, Wilcoxon, và power analysis;
- từng tác giả phải giải thích được vì sao cần khoảng 30-35 paired folds để có
  power thông thường cho hiệu ứng khoảng `d_z = 0.5`;
- từng tác giả phải tự nói được đóng góp dương của bài mà không nhìn giấy.

Đã thêm checklist ôn vấn đáp:

- Markdown: `docs/author_mastery_checklist.md`
- Word tiếng Việt: `docs/author_mastery_checklist_vi.docx`

Lưu ý: checklist chỉ hỗ trợ học. Bài chỉ nên nộp sau khi từng tác giả thật sự
trả lời được phần thầy hỏi miệng.

## 5. Sufficiency theo ERASER

Đã kiểm lại quy ước dấu và sửa phần diễn giải trong bài.

Bài hiện định nghĩa:

`Sufficiency = f(x)_c - f(x_top-k)_c`.

Theo quy ước này, sufficiency càng thấp càng tốt, vì rationale-only input càng
giữ được score gốc thì chênh lệch càng nhỏ. Giá trị âm có nghĩa là
rationale-only input nhận score cao hơn full input.

Số liệu hiện tại:

| Explainer | Comprehensiveness | Random comp. | Sufficiency | Random suff. | Ratio comp. | Ratio suff. |
|---|---:|---:|---:|---:|---:|---:|
| Contrastive projection intrinsic | 0.0305 | 0.0059 | -0.0395 | 0.0337 | 5.21x | -1.17x |
| TF-IDF Linear SVM coefficients | 0.0867 | 0.0216 | 0.0484 | 0.1141 | 4.01x | 0.42x |

Diễn giải đã được làm thận trọng hơn: sufficiency âm có thể cho thấy các token
ngoài rationale làm nhiễu score của model, nhưng không được dùng như bằng
chứng rằng explanation chắc chắn hữu ích với con người. Claim được giới hạn ở
model faithfulness.

## 6. Artifact ẩn danh

Artifact đã được dựng lại bằng:

`scripts/make_review_artifact.ps1`

File artifact:

`artifacts/nfr_eai_fisat_2026_review_artifact.zip`

Đã kiểm:

- link anonymous trả HTTP `200 OK`;
- artifact local được giải nén và scan;
- package submission mới được scan;
- không thấy tên tác giả, email, link GitHub gốc, local paths, hoặc file
  camera-ready có tên tác giả;
- lỗi metadata cũ trong `reports/run_all_experiments_summary.md` đã sửa: file
  này không còn ghi absolute local path, chỉ ghi portable `python ...` command.

Việc nhóm vẫn phải tự làm trước khi nộp:

- mở link anonymous bằng incognito browser thật;
- kiểm README;
- kiểm file tree;
- kiểm comment code;
- kiểm history/metadata mà reviewer nhìn thấy;
- xác nhận không lộ tên nhóm, "FPT", email, hoặc link gốc.

## File giao lại

- `.tex` đã sửa: `paper/main.tex`
- PDF đã build: `paper/main.pdf`
- Số trang body sau khi cắt: tối đa 14 trang
- Tổng PDF: 15 trang
- Kết quả DistilBERT trong bảng: chỉ Table `tab:nice-per-label`
- Giải trình mục 2 và mục 5: nằm trong tài liệu này
- Artifact: `artifacts/nfr_eai_fisat_2026_review_artifact.zip`
- Package mới nhất: `submission/fisat2026_review_20260713_222340`
