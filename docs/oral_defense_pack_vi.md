# Oral Defense Pack - Proposition 2 và phân tích power

## Cổng bắt buộc trước khi nộp

Tài liệu này dùng để học và tự kiểm tra, không phải bằng chứng rằng tác giả đã
làm chủ bài. Từng tác giả chỉ được tự đánh dấu đạt khi có thể giải thích bằng
lời của mình, không đọc tài liệu và trả lời được câu hỏi phản biện.

**BLOCKER - TÁC GIẢ PHẢI HỌC LẠI HOẶC LOẠI KHỎI BÀI:** nếu bất kỳ tác giả nào
không giải thích được Proposition 2 hoặc nguồn của con số power 34 cặp độc lập,
bài chưa sẵn sàng nộp theo yêu cầu của người hướng dẫn.

## 1. Proposition 2 bằng lời

Với mẫu `i`, mô hình positive projection tạo vector điểm thô
`u_i = p_i M'`. Sau đó `_minmax_rows` lấy điểm nhỏ nhất và lớn nhất trong
chính vector nhãn của mẫu đó để đưa mọi điểm về `[0, 1]`:

`s_i,l = (u_i,l - min_k u_i,k) / (max_k u_i,k - min_k u_i,k)`.

Phép biến đổi này tăng nghiêm ngặt theo `u_i,l` khi `max > min`, nên không đổi
thứ hạng các nhãn trong cùng một mẫu. Tuy nhiên, quyết định nhị phân sau một
global threshold `tau` không còn là phép cắt độc lập trên riêng `u_i,l`, vì
ngưỡng tương đương trên thang điểm thô là:

`tau_i = min_k u_i,k + tau (max_k u_i,k - min_k u_i,k)`.

Do `min` và `max` được tính từ toàn bộ nhãn của mẫu `i`, điểm của các nhãn khác
có thể đổi `tau_i` và đổi quyết định cho nhãn `l` dù `u_i,l` giữ nguyên.

## 2. Chứng minh từng bước

1. Đặt `a_i = min_k u_i,k`, `b_i = max_k u_i,k` và giả sử `b_i > a_i`.
2. Khi đó `s_i,l = (u_i,l-a_i)/(b_i-a_i)`.
3. Với một mẫu `i` cố định, mọi nhãn dùng cùng hệ số dương
   `1/(b_i-a_i)` và cùng hằng số `-a_i/(b_i-a_i)`.
4. Vì đây là biến đổi affine tăng nghiêm ngặt,
   `s_i,k >= s_i,l` khi và chỉ khi `u_i,k >= u_i,l`: thứ hạng được giữ nguyên.
5. Giải bất đẳng thức `s_i,l >= tau`:
   `u_i,l >= a_i + tau(b_i-a_i) = tau_i`.
6. `a_i` và `b_i` phụ thuộc vào toàn bộ `{u_i,k}`, không chỉ `u_i,l`; vì vậy
   đây là threshold theo mẫu, không phải cutoff raw-score cố định theo nhãn.
7. Nếu `b_i = a_i`, code đặt mẫu số thành 1 rồi trả mọi `s_i,l = 0`; với
   `tau > 0` không nhãn nào được dự đoán.
8. Khi `lambda=0`, `u_i,l=<l|r_i>^2`. TF-IDF và positive centroid không âm,
   nên bình phương vẫn giữ thứ hạng cosine. Kết luận này không áp dụng cho
   contrastive projection có biên độ âm trước rectification.

Ví dụ kiểm tra nhanh với `tau=0.5`:

- `u=(0.5, 0.0)` biến thành `s=(1, 0)`: nhãn 1 được chọn.
- `u=(0.5, 0.9)` biến thành `s=(0, 1)`: cùng raw score 0.5 cho nhãn 1 nhưng
  nhãn 1 không được chọn.

## 3. Hai nguồn coupling và vì sao độc lập về cơ chế

### Coupling từ `M'`

`M'=(1-lambda)I+lambda M`, nên:

`u_l=(1-lambda)p_l + lambda sum_k p_k M_kl`.

Các phần tử ngoài đường chéo làm điểm nhãn `l` phụ thuộc trực tiếp vào điểm
`p_k` của nhãn khác và thống kê đồng xuất hiện. Cơ chế này xảy ra trước
thresholding và vẫn tồn tại nếu bỏ row-wise normalization.

### Coupling từ row-wise normalization

Ngay cả khi `lambda=0` và `M'=I`, global threshold trên `s_i,l` tương đương
raw threshold `tau_i` phụ thuộc vào `min/max` của mọi nhãn trong mẫu. Cơ chế
này xảy ra sau khi tạo điểm và vẫn tồn tại khi không có interference.

Hai nguồn độc lập về cơ chế vì có thể bật một nguồn và tắt nguồn kia. Cần nói
đúng phạm vi: row-wise min-max chỉ được dùng trong
`QuantumInspiredNFRClassifier` (positive projection). Contrastive và hybrid
dùng sigmoid/calibration rồi clip, nên Proposition 2 không áp dụng cho hai biến
thể đó.

## 4. Giả định, trường hợp biên và phản biện có thể gặp

- `max > min` là điều kiện để có biến đổi affine tăng nghiêm ngặt.
- Kết luận cosine ranking ở `lambda=0` cần positive TF-IDF states và positive
  centroids để inner product không âm.
- Proposition 2 nói về thứ hạng và decision coupling, không chứng minh tăng
  accuracy.
- Interference có ý nghĩa toán học nhưng ablation hiện tại không cho thấy lợi
  ích accuracy; nó gần như trung tính với positive projection và gây hại cho
  contrastive projection.
- Gọi các nguồn coupling là "independent" nghĩa là độc lập về cơ chế/tồn tại,
  không phải độc lập thống kê giữa các biến ngẫu nhiên.
- Reviewer có thể hỏi vì sao gọi điểm là probability. Câu trả lời: không gọi là
  probability; đó là association/calibrated score và không bị buộc tổng bằng 1.

## 5. Paired Cohen's `d_z`

Với mỗi fold có một cặp kết quả của model A và B, đặt `d_j=A_j-B_j`. Khi đó:

`d_z = mean(d_j) / sd(d_j)`.

`d_z` chuẩn hóa độ chênh bằng độ lệch chuẩn của **chính các chênh lệch ghép
cặp**. Nó khác Cohen's `d` cho hai nhóm độc lập, vốn dùng pooled standard
deviation giữa hai nhóm. Nó cũng khác các biến thể paired effect size dùng độ
lệch chuẩn của từng lần đo hoặc điều chỉnh theo tương quan. Vì thiết kế ở đây
so hai model trên cùng folds, `d_z` là mô tả tự nhiên, nhưng `n=5` quá nhỏ để
ước lượng ổn định và các fold CV không độc lập hoàn toàn.

## 6. Tái tạo power analysis

Giả định được công khai trong bài:

- test: paired t-test hai phía;
- effect size: `|d_z|=0.5`;
- `alpha=0.05`;
- target power `1-beta=0.80`;
- các cặp được giả định độc lập trong phép tính power lý tưởng hóa.

Với `n` cặp, noncentrality parameter là `delta=d_z*sqrt(n)`, bậc tự do
`df=n-1`, và ngưỡng tới hạn là `t_(1-alpha/2,df)`. Power là xác suất của phân
phối noncentral-t rơi ngoài hai ngưỡng. Duyệt `n` cho kết quả nhỏ nhất là
`n=34`, với power xấp xỉ `0.8078` (n=33 chỉ khoảng `0.7954`).

Chạy lại từ thư mục gốc:

```powershell
.\.venv\Scripts\python.exe scripts\reproduce_statistical_analysis.py
```

Bằng chứng đầu ra:

- `reports/quantum_contribution_effect_sizes.csv`;
- `reports/power_analysis.csv`.

Không được diễn giải kết quả này thành "hãy chạy 34-fold CV". Các fold từ cùng
một dataset có train sets chồng lắp và không phải 34 quan sát độc lập. Con số 34
chỉ cho thấy 5 paired folds hiện tại có power thấp dưới giả định thuận lợi; bằng
chứng mạnh hơn cần repeated evaluation được thiết kế cẩn thận và, quan trọng
hơn, dataset độc lập.

## 7. Mười câu hỏi miệng và đáp án tự chấm

Mỗi câu chấm `0/1/2`: `0` không trả lời được; `1` đúng ý nhưng thiếu điều kiện;
`2` đúng, đủ và nói bằng lời của mình. Phải đạt ít nhất `18/20`, và câu 4, 5,
8, 9 không được 0.

1. **`M'` làm gì?**
   - Đáp án: trộn identity với ma trận đồng xuất hiện; phần tử ngoài đường chéo
     truyền score giữa các nhãn trước normalization/thresholding.
2. **Row-wise min-max có đổi thứ hạng nhãn trong cùng mẫu không?**
   - Đáp án: không khi `max>min`, vì đó là cùng một biến đổi affine tăng cho
     mọi nhãn của mẫu.
3. **Vì sao giữ thứ hạng nhưng vẫn đổi quyết định nhị phân?**
   - Đáp án: global threshold trên normalized score trở thành `tau_i` trên raw
     score, và `tau_i` thay đổi theo profile điểm của mẫu.
4. **`tau_i` phụ thuộc nhãn khác bằng cách nào?**
   - Đáp án: qua `min_k u_i,k` và `max_k u_i,k`; ít nhất một trong hai thường do
     nhãn `k != l` quyết định.
5. **Vì sao normalization coupling độc lập với `M'`?**
   - Đáp án: đặt `lambda=0` vẫn còn `tau_i`; ngược lại bỏ normalization vẫn còn
     các tổng ngoài đường chéo trong `pM'`.
6. **Proposition 2 áp dụng cho model nào?**
   - Đáp án: positive-projection model dùng `_minmax_rows`; không áp dụng trực
     tiếp cho contrastive/hybrid dùng sigmoid và clip.
7. **`d_z=0.49` trong bài đến từ đâu?**
   - Đáp án: mean chênh Macro-F1 theo 5 cặp fold giữa Hybrid alpha=0.30 và
     SVM-only cùng TF-IDF backbone, chia cho SD của 5 chênh lệch.
8. **Tại sao ra 34?**
   - Đáp án: giải power của paired t-test hai phía với `d_z=0.5`, alpha 0.05,
     power 0.80 bằng noncentral-t; n=34 cho power khoảng 0.8078.
9. **Tại sao không tăng lên 34 folds trên NICE?**
   - Đáp án: folds trên cùng dữ liệu phụ thuộc và train sets chồng lắp; giả định
     cặp độc lập của power calculation không được đáp ứng.
10. **Kết luận accuracy trung thực nhất là gì?**
    - Đáp án: hybrid có chênh lệch dương nhỏ so với TF-IDF/SVM-only nhưng chưa
      có ý nghĩa thống kê; đóng góp chính là scoring/explainability/diagnostic,
      không phải state-of-the-art accuracy.

## 8. Phiếu xác nhận của từng tác giả

- [ ] Tôi đã chạy script thống kê và đối chiếu hai CSV đầu ra.
- [ ] Tôi tự khai triển được Proposition 2 trên giấy.
- [ ] Tôi trả lời đạt ít nhất 18/20 mà không nhìn tài liệu.
- [ ] Tôi hiểu phần nào do AI hỗ trợ và xác nhận khai báo cuối bài là đúng sự thật.
- [ ] Tôi sẵn sàng trả lời trực tiếp người hướng dẫn.

Tên tác giả: ____________________  Ngày: __________  Điểm tự kiểm tra: ____/20
