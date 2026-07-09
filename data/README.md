# Data Guide

Không commit trực tiếp dataset nếu license không cho phép.

## Dataset nên tải

1. NICE: Non-Functional Requirements Identification, Classification, and Explanation
2. PROMISE / Tera-PROMISE NFR
3. PROMISE_exp
4. Software Requirements Classification merged datasets

## Checksum của file đang dùng để sinh số liệu trong paper (2026-07-09)

`data/raw/PROMISE-relabeled-NICE.csv`:
- SHA256: `87acb2172bc6273b8e04c55b4de8bf090cb0a9980b9d23010b20af88245f2642`
- Kích thước: 95725 bytes, 622 dòng thô, còn 381 dòng sau khi lọc (11 nhãn NFR, label cardinality 1.3648).

`data/raw/PROMISE_exp.arff`:
- SHA256: `7475c2904648912ef08bd1b6149f505f7ce6ab26ee9b187c2ddee28d1af97d75`
- Kích thước: 115622 bytes.
- Nguồn: `https://raw.githubusercontent.com/AleksandarMitrevski/se-requirements-classification/master/0-datasets/PROMISE_exp/PROMISE_exp.arff`.

Hai file raw này bị `.gitignore`, nên nếu tải lại từ nguồn công khai và checksum
không khớp, các số liệu trong `paper/main.tex`/`reports/` có thể không tái tạo
được chính xác. Bản review artifact đóng kèm cả hai file tại:

- `data/raw/PROMISE-relabeled-NICE.csv`
- `data/raw/PROMISE_exp.arff`

## Định dạng CSV chuẩn cho project

File xử lý nên có dạng:

```csv
id,text,security,performance,usability,reliability,maintainability,portability,operational,scalability
REQ_001,"The system shall encrypt user passwords.",1,0,0,0,0,0,0,0
```

Trong đó:

- `id`: mã requirement
- `text`: nội dung requirement
- Các cột còn lại: nhãn đa lớp, giá trị `0` hoặc `1`

