# Reviewer Response — A1–A5

Trả lời từng điểm trong `NHAN_XET_BAI_NFR_FISAT_2026.md`, mục A (A1–A5). Mỗi mục nêu: đã làm gì, số liệu chạy được, và thay đổi cụ thể trong `paper/main.tex`. Số liệu lấy trực tiếp từ `reports/*.csv` sau khi chạy lại toàn bộ pipeline trên môi trường pin cứng version (`requirements-lock.txt`, xem "Ghi chú reproducibility" ở cuối file).

---

## A1 — Mâu thuẫn interference (lý thuyết vs ablation)

**Yêu cầu ban đầu:** chạy ablation interference bật/tắt cho cả positive projection (không chỉ contrastive), trả lời dứt khoát interference có giúp gì không, và hạ nó xuống đúng vai trò thật trong cả lý thuyết lẫn phần viết.

**Đã làm:**
- Chạy `run_nice_ablation_experiment.py` với 4 cấu hình: positive có/không interference, contrastive có/không interference (5-fold CV).
- Số liệu (Macro-F1 ± std, `reports/nice_ablation_summary.csv`):

| Biến thể | Không interference | Có interference | Chênh lệch |
|---|---|---|---|
| Positive projection | 0.5526 ± 0.0285 | 0.5490 ± 0.0237 | −0.0037 (không đáng kể) |
| Contrastive projection | 0.5397 ± 0.0398 | 0.4118 ± 0.0275 | **−0.1279** (hại rõ rệt) |

- Kiểm định paired Wilcoxon cho contrastive: 5/5 fold đều xấu đi khi bật interference, $p=0.0625$ (nhỏ nhất có thể ở $n=5$ fold), Cohen's $d_z=-2.89$ — hiệu ứng lớn, nhất quán.

**Thay đổi trong `main.tex`:**
- Table `tab:nice-ablation` giờ có đủ cả 2 dòng positive (có/không interference) — trước đây thiếu dòng "without interference".
- Ablation interpretation (§Ablation Study): nêu rõ "interference provides no measurable benefit for either projection variant... substantially worsens the contrastive projection."
- Introduction (danh sách đóng góp): không còn liệt kê interference như một trụ cột đóng góp không điều kiện — sửa thành "a label-coupling formulation via an interference term, which later experiments show is only marginally active in practice."
- Hyperparameter table vẫn giữ $\lambda=0.15$ (positive) / $0.05$ (contrastive) / $0.03$ (hybrid) làm giá trị đã dùng để tạo số liệu, không đổi giá trị mặc định — chỉ đổi cách paper *nói* về vai trò của nó.

**Kết luận:** interference không còn được trình bày như đóng góp chính; được giữ lại chủ yếu vì công thức toán (Proposition "Interference as label coupling") độc lập thú vị, không phải vì nó cải thiện accuracy.

---

## A2 — Đóng góp "quantum" có thật không?

**Yêu cầu ban đầu:** định lượng chính xác phần tăng thêm do quantum, kèm bootstrap, kiểm định thống kê, effect size; nếu không có ý nghĩa thì tái định vị bài quanh interpretability.

**Đã làm:** tách rõ hai câu hỏi khác nhau — "quantum đứng một mình có cạnh tranh không" và "quantum fusion vào SVM có giúp không" — và kiểm định riêng từng câu bằng paired Wilcoxon, Cohen's $d_z$, rank-biserial $r$, và bootstrap (script lưu tại `reports/quantum_contribution_effect_sizes.csv`).

| So sánh | Δ Macro-F1 | Cohen's $d_z$ | Wilcoxon $p$ | Kết luận |
|---|---|---|---|---|
| Contrastive Projection − SVM (đứng một mình) | −0.1931 | **−5.92** | 0.0625 | Thua rõ rệt, 5/5 fold |
| Positive Projection − SVM (đứng một mình) | −0.0559 | **−1.36** | 0.0625 | Thua rõ rệt, 5/5 fold |
| Hybrid − SVM-only (cùng backbone TF-IDF, cô lập đúng phần quantum thêm vào) | +0.0140 | 0.49 | 0.3125 | Dương nhưng mong manh — âm ở 2/5 fold |
| Hybrid − TF-IDF SVM (bảng chính) | +0.0035 | 0.73 | 0.1875 | Không có ý nghĩa thống kê |
| Hybrid − TF-IDF LR (bảng chính) | +0.0107 | 0.54 | 0.4375 | Không có ý nghĩa thống kê |
| Hybrid − Contrastive Projection (giá trị của fusion) | +0.1967 | 6.59 | 0.0625 (CV) / **<0.001 (bootstrap)** | Rõ ràng, mạnh — nhưng nói về việc quantum quá yếu để đứng một mình, không phải về việc SVM cần quantum |

Bootstrap trên tập test held-out (`reports/nice_paired_bootstrap_summary.csv`, 2000 lần resample): Hybrid vs TF-IDF SVM: +0.0081, CI $[-0.0100, 0.0263]$; Hybrid vs TF-IDF LR: +0.0020, CI $[-0.0205, 0.0227]$ — cả hai khoảng đều vắt qua 0.

Power analysis: để phát hiện ổn định hiệu ứng $d_z\approx0.5$ cần khoảng 30–35 fold ghép cặp, không khả thi với 1 dataset 381 dòng dùng 5-fold CV.

**Thay đổi trong `main.tex`:**
- Abstract, Discussion, Conclusion viết lại toàn bộ: không còn khẳng định "competitive with TF-IDF baselines" như một kết luận đã xác nhận — thay bằng "small, directionally positive, and not statistically significant"; nêu rõ số $d_z$, $p$-value, CI ngay trong văn bản.
- Đóng góp của bài được định vị lại quanh: (1) interpretability nội tại, (2) một phát hiện chẩn đoán (quantum đứng một mình yếu, interference phản tác dụng), (3) fusion là kết quả gợi ý (suggestive), không phải đã xác nhận (confirmed).

**Kết luận:** không có cấu hình nào trong dữ liệu hiện tại hậu thuẫn được tuyên bố "quantum đóng góp thật vào accuracy" ở $n=5$ fold / 381 mẫu — đây là vấn đề power nhiều bằng vấn đề effect. Bài đã nói thẳng điều này thay vì né tránh.

---

## A3 — Bằng chứng chỉ dựa trên một dataset nhỏ

**Yêu cầu ban đầu:** thêm dataset thứ hai hoặc baseline transformer fine-tuned; nếu để future work thì phải có lập luận thuyết phục bằng chữ.

**Đã làm:**
- Xác nhận lại bằng số: thí nghiệm phụ trên PROMISE-expanded (525 dòng, single-label) đã có sẵn, số liệu khớp đúng `reports/promise_exp_metrics.csv` (0.7025 accuracy / 0.6748 Macro-F1 cho quantum projection vs 0.6899 / 0.6344 cho TF-IDF LR).
- **Không** thêm dataset multi-label thứ hai, **không** thêm baseline transformer fine-tuned trong phiên làm việc này — đây vẫn là giới hạn thật, không giả vờ đã giải quyết.

**Thay đổi trong `main.tex`:**
- Threats to Validity: bỏ tuyên bố tuyệt đối "NICE is currently the only publicly available dataset" → hạ thành "to the best of our knowledge... at the time of writing".
- Bỏ "verify generalizability... successfully generalized" (ngụ ý đã chứng minh tổng quát hóa) → thay bằng "the projection model remained competitive... on one split", kèm câu nói rõ: PROMISE-expanded là single-label nên **không** kiểm chứng được cơ chế multi-label/interference — không được phép đọc như bằng chứng tổng quát hóa cho phần đóng góp chính.
- Auxiliary PROMISE-expanded Result (§4.8): thêm caveat "single split, không cross-validation, không kiểm định ý nghĩa" — trước đây thiếu caveat này dù đoạn NICE single-split ngay phía trên có.

**Kết luận:** đây là mục **chưa giải quyết bằng thực nghiệm mới** — chỉ giải quyết bằng cách viết trung thực hơn về giới hạn của bằng chứng đã có. Threats to Validity đã liệt kê rõ baseline còn thiếu (fine-tuned BERT/RoBERTa/NoRBERT/ML-kNN) như một giới hạn công khai, không che giấu.

---

## A4 — Hai Proposition có mô tả đúng cách model hoạt động không?

**Yêu cầu ban đầu:** kiểm lại từng mệnh đề, đặc biệt Proposition 1 (ranking-equivalence) có thật sự mô tả đúng cách model ra quyết định (multi-label, ngưỡng theo từng nhãn) không.

**Đã làm:** đọc `predict_proba()` trong `quantum_model.py` và phát hiện: hàm này **luôn luôn** áp row-wise min-max normalization trước khi threshold, bất kể $\lambda$ — Proposition 1 gốc chỉ chứng minh cho điểm số thô $s_c(r)=\langle c|r\rangle^2$, tức mô tả sai bước cuối cùng thực sự được dùng để ra quyết định.

**Thay đổi trong `main.tex`:** thay hoàn toàn Proposition 1 bằng bản mới, có chứng minh và phản ví dụ số cụ thể:

- **Phần đúng, giữ lại:** min-max theo hàng là affine tăng ngặt trong cùng một instance, nên **thứ hạng** nhãn trong-instance được bảo toàn (LRAP không bị ảnh hưởng); ở $\lambda=0$, thứ hạng này trùng thứ hạng cosine similarity — đây là phần "tinh thần" của Proposition 1 cũ, giờ được chứng minh đúng phạm vi của nó.
- **Phần sai, đã sửa:** ngưỡng quyết định thực tế phụ thuộc vào $\min_k, \max_k$ của **từng instance** — không tương đương một ngưỡng cosine cố định như tuyên bố cũ. Thêm phản ví dụ 2 nhãn cụ thể: cùng điểm thô $u_1=0.5$ nhưng hai instance khác nhau (do nhãn còn lại khác nhau) ra hai quyết định trái ngược.
- Đặt hai Proposition theo đúng thứ tự phụ thuộc (interference trước, ranking-invariance sau, vì cái sau dùng điểm số đã qua interference của cái trước).
- Đã kiểm tra: cân bằng `\begin`/`\end` cho `proposition`/`proof`/`remark` (2/2/1), không còn khối trùng lặp, tất cả `\ref`/`\label` khớp.

**Kết luận:** Proposition 1 giờ mô tả đúng 100% những gì `predict_proba()` thực sự làm — không còn khoảng cách giữa toán và code.

---

## A5 — Explainability đánh giá còn nông?

**Yêu cầu ban đầu:** bổ sung comprehensiveness/sufficiency theo ERASER, không chỉ deletion test tự tham chiếu vào điểm số của chính model.

**Đã làm:**
- Cài đặt cả hai chỉ số ERASER: Comprehensiveness và Sufficiency, có random-deletion control, tính trên 158 label assignment thật trong tập test, so sánh với baseline SVM TF-IDF coefficients để có phép so sánh công bằng (cùng dữ liệu, cùng luồng RNG — `run_nice_robustness_experiment.py`).
- Số liệu (`reports/nice_deletion_comparison_summary.csv`):

| | Comprehensiveness | vs random | Sufficiency | vs random |
|---|---|---|---|---|
| Contrastive Projection | 0.0305 | 5.21× | −0.0395 | −1.17× |
| TF-IDF Linear SVM (coefficients) | 0.0867 | 4.01× | 0.0484 | 0.42× |

**Thay đổi trong `main.tex`:** câu kết luận cũ "highly faithful and competitive with classical attribution baselines" phóng đại theo nghĩa tuyệt đối (SVM thực ra loại bỏ nhiều điểm số hơn hẳn về giá trị tuyệt đối, 0.0867 vs 0.0305) — đã sửa lại chính xác hơn: "competitive on a relative, random-normalized basis rather than as uniformly stronger."

**Kết luận:** đánh giá giờ dùng đúng khung ERASER chuẩn (không chỉ deletion-test tự chế), và câu diễn giải không còn phóng đại theo chiều tuyệt đối.

---

## Ghi chú reproducibility (nền tảng cho mọi số liệu ở trên)

Toàn bộ số liệu A1–A5 phía trên được sinh ra **thật sự chạy lại**, không phải đọc code suông:
- Cài Python 3.12.10 + `scikit-learn==1.9.0` (pin cứng trong `requirements-lock.txt`), vì phiên bản không pin trước đây khiến `StratifiedKFold`/`train_test_split` cho split khác nhau dù cùng seed.
- Sửa `LinearSVC` thiếu `random_state` ở 6 chỗ → xác nhận determinism 100% (chạy 2 lần độc lập, kết quả giống bit-for-bit).
- Dataset dùng để tái tạo: `data/raw/PROMISE-relabeled-NICE.csv`, SHA256 ghi trong `data/README.md`.

## Chưa xử lý / còn để ngỏ

- A3: chưa chạy dataset multi-label thứ hai hoặc fine-tuned transformer baseline (giới hạn thời gian/phạm vi phiên này, đã ghi rõ trong Threats to Validity).
- Nhóm B (tuân thủ hội nghị: ẩn danh, artifact, khai báo AI, số trang) đã audit ở vòng trước, không nằm trong phạm vi file này.
