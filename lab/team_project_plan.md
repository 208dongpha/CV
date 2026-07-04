# Kế hoạch nhóm - Đồ án phân loại rác tái chế

## 1. Tên đề tài

**Xây dựng và đánh giá hiệu quả các thuật toán trong bài toán phân loại hình ảnh rác tái chế.**

## 2. Ý tưởng chính

Nhóm không chỉ làm một app dự đoán loại rác. Mục tiêu chính là đánh giá xem các kỹ thuật xử lý ảnh trong môn học có giúp cải thiện kết quả phân loại rác hay không.

Câu hỏi nghiên cứu:

```text
Nếu cùng dùng HOG + SVM để phân loại rác, việc thêm K-means segmentation
và contour/shape features có làm accuracy hoặc macro-F1 tốt hơn không?
```

Các lớp rác dự kiến:

- `plastic`
- `paper`
- `cardboard`
- `glass`
- `metal`
- `trash/organic`

## 3. Vì sao đề tài hợp yêu cầu lab_CK?

Đề tài dùng dữ liệu thật, có baseline, có thuật toán so sánh, có metric định lượng và có ảnh trung gian.

Các chương được dùng:

- **Chương 2:** tiền xử lý ảnh: resize, blur, chuẩn hóa màu, CLAHE.
- **Chương 4:** phân đoạn ảnh bằng K-means clustering và morphology.
- **Chương 3:** contour và shape features: area, perimeter, aspect ratio, circularity, extent, solidity.
- **Chương 5:** nhận dạng ảnh bằng HOG + SVM.

Như vậy đề tài có đủ ít nhất 3 kỹ thuật, trong đó có nhiều kỹ thuật thuộc Chương 3/4/5, đúng yêu cầu của thầy.

## 4. Pipeline tổng quát

```text
Ảnh rác đầu vào
        |
        v
Ch.2 - Tiền xử lý ảnh
resize, Gaussian blur, CLAHE, chuẩn hóa màu
        |
        v
Ch.4 - K-means segmentation
phân cụm pixel theo màu RGB/HSV/Lab
        |
        v
Morphology
opening, closing để làm sạch mask
        |
        v
Ch.3 - Contour
tìm contour lớn nhất, bounding box, crop vật thể
        |
        v
Shape features
area, perimeter, aspect ratio, circularity, extent, solidity
        |
        v
HOG feature
histogram of oriented gradients
        |
        v
Ch.5 - SVM classifier
phân loại rác
        |
        v
Metric
accuracy, macro-F1, confusion matrix
```

## 5. Bốn cấu hình thí nghiệm

Không phải làm 4 project riêng. Nhóm chỉ viết một bộ hàm chung, sau đó bật/tắt segmentation và shape features để chạy 4 cấu hình.

| Cấu hình | Pipeline | Mục đích |
|---|---|---|
| Baseline 1 | Ảnh gốc -> Resize -> HOG -> SVM | Mốc cơ bản, không segmentation |
| Baseline 2 | Ảnh gốc -> Resize -> HOG + shape features -> SVM | Kiểm tra shape features khi chưa crop |
| Proposed 1 | Ảnh gốc -> K-means -> contour crop -> HOG -> SVM | Kiểm tra tác dụng của segmentation/crop |
| Proposed 2 | Ảnh gốc -> K-means -> contour crop -> HOG + shape features -> SVM | Pipeline chính của nhóm |

Code nên thiết kế bằng option:

```python
use_segmentation = True / False
use_shape_features = True / False
```

## 6. Tham số cần khảo sát

Theo yêu cầu lab_CK, mỗi kỹ thuật chính nên có khảo sát tham số ít nhất 3 giá trị.

### K-means segmentation

- Số cụm `k`: `2`, `3`, `4`, `5`
- Không gian màu: `RGB`, `HSV`, `Lab`

### Morphology

- Kernel: `3x3`, `5x5`, `7x7`

### Contour

- Min area: `100`, `500`, `1000` pixel
- Có hoặc không dùng shape features

### HOG

- Orientations: `6`, `9`, `12`
- Pixels per cell: `(8,8)`, `(16,16)`

### SVM

- `C`: `0.1`, `1`, `10`
- Kernel: `linear`, `rbf`

## 7. Metric đánh giá

Metric chính:

- Accuracy
- Macro precision
- Macro recall
- Macro F1-score
- Per-class F1-score
- Confusion matrix

Vì dataset rác có thể lệch lớp, nhóm không nên chỉ dùng accuracy. Macro-F1 quan trọng hơn vì nó đánh giá đều trên từng lớp.

## 8. Dữ liệu

Dataset đề xuất:

- TrashNet
- Kaggle Garbage Classification
- Có thể tự chụp thêm ảnh bằng điện thoại để demo Streamlit

Cấu trúc thư mục gợi ý:

```text
data/
  garbage/
    train/
      plastic/
      paper/
      cardboard/
      glass/
      metal/
      trash/
    val/
      plastic/
      paper/
      cardboard/
      glass/
      metal/
      trash/
    test/
      plastic/
      paper/
      cardboard/
      glass/
      metal/
      trash/
```

## 9. Chia việc cho 7 thành viên

### Thành viên 1 - Trưởng nhóm + tích hợp notebook

Nhiệm vụ:

- Quản lý timeline.
- Gom code từ các thành viên.
- Đảm bảo notebook chạy từ đầu đến cuối.
- Kiểm tra các phần có đúng pipeline không.
- Chuẩn bị kịch bản thuyết trình.

Deliverables:

- Notebook bản cuối.
- Checklist tiến độ.
- Slide/kịch bản demo tổng thể.

### Thành viên 2 - Dataset + data exploration

Nhiệm vụ:

- Tải/chọn dataset.
- Chia train/val/test.
- Kiểm tra số lượng ảnh mỗi lớp.
- Hiển thị ảnh mẫu từng lớp.
- Ghi nguồn dataset và lý do chọn dataset.

Deliverables:

- Thư mục dataset sạch.
- Bảng số lượng ảnh mỗi lớp.
- Một cell notebook hiển thị ảnh mẫu.

### Thành viên 3 - Tiền xử lý ảnh + K-means segmentation

Nhiệm vụ:

- Viết hàm resize, chuẩn hóa màu, blur/CLAHE.
- Viết hàm K-means segmentation.
- Thử `k = 2, 3, 4, 5`.
- Thử không gian màu `RGB`, `HSV`, `Lab`.
- Lưu ảnh trung gian: ảnh gốc, ảnh sau K-means, mask.

Deliverables:

- Hàm `preprocess_image()`.
- Hàm `kmeans_segment()`.
- Bảng/ảnh parameter sweep của K-means.

### Thành viên 4 - Morphology + contour + crop

Nhiệm vụ:

- Làm sạch mask bằng opening/closing.
- Tìm contour lớn nhất.
- Tính bounding box.
- Crop vật thể rác.
- Trích shape features: area, perimeter, aspect ratio, circularity, extent, solidity.

Deliverables:

- Hàm `clean_mask()`.
- Hàm `extract_largest_contour()`.
- Hàm `crop_object()`.
- Hàm `extract_shape_features()`.
- Ảnh minh họa contour và crop.

### Thành viên 5 - HOG feature + SVM baseline

Nhiệm vụ:

- Viết hàm trích HOG.
- Train Baseline 1: ảnh gốc -> HOG -> SVM.
- Train Baseline 2: ảnh gốc -> HOG + shape features -> SVM.
- Sweep HOG và SVM.

Deliverables:

- Hàm `extract_hog_features()`.
- Hàm `train_svm()`.
- Kết quả baseline 1 và baseline 2.
- Bảng sweep HOG/SVM.

### Thành viên 6 - Proposed pipeline + đánh giá định lượng

Nhiệm vụ:

- Chạy Proposed 1 và Proposed 2.
- Tính accuracy, precision, recall, macro-F1.
- Vẽ confusion matrix.
- So sánh baseline vs proposed.
- Phân tích lớp nào hay bị nhầm.

Deliverables:

- Bảng metric 4 cấu hình.
- Confusion matrix.
- Nhận xét kết quả.
- Cell hiển thị ảnh dự đoán đúng/sai.

### Thành viên 7 - Streamlit demo + báo cáo

Nhiệm vụ:

- Làm app Streamlit upload ảnh.
- Load model đã train.
- Hiển thị ảnh gốc, mask/crop, kết quả dự đoán.
- Gợi ý nhóm rác: tái chế/hữu cơ/rác còn lại.
- Hỗ trợ viết báo cáo phần ứng dụng thực tế và demo.

Deliverables:

- `app.py`.
- Demo upload ảnh chụp bằng điện thoại.
- Screenshot giao diện.
- Phần mô tả demo trong báo cáo.

## 10. Timeline đề xuất

### Giai đoạn 1 - Chuẩn bị dữ liệu

- Chọn dataset.
- Chia train/val/test.
- Hiển thị ảnh mẫu.
- Kiểm tra class imbalance.

### Giai đoạn 2 - Xây pipeline xử lý ảnh

- Tiền xử lý ảnh.
- K-means segmentation.
- Morphology.
- Contour crop.
- Shape features.

### Giai đoạn 3 - Train và so sánh model

- Train baseline 1.
- Train baseline 2.
- Train proposed 1.
- Train proposed 2.
- Chạy parameter sweep.

### Giai đoạn 4 - Đánh giá và viết báo cáo

- Bảng metric.
- Confusion matrix.
- Ảnh đúng/sai.
- Thảo luận giả thuyết đúng/sai.
- Viết kết luận.

### Giai đoạn 5 - Demo

- Streamlit app.
- Upload ảnh điện thoại.
- Chạy dự đoán.
- Chuẩn bị thuyết trình.

## 11. Cấu trúc notebook nên có

```text
1. Problem Statement & Hypothesis
2. Dataset Loading & Exploration
3. Preprocessing
4. K-means Segmentation
5. Morphology + Contour + Crop
6. Shape Feature Extraction
7. HOG Feature Extraction
8. SVM Training
9. Baseline Experiments
10. Proposed Experiments
11. Parameter Sweep
12. Evaluation Metrics
13. Confusion Matrix
14. Error Analysis
15. Streamlit Demo Note
16. Discussion & Conclusion
```

## 12. Kết quả cần có trong báo cáo

- Bảng so sánh 4 cấu hình.
- Confusion matrix.
- Biểu đồ parameter sweep.
- Ảnh trung gian của pipeline.
- Ví dụ dự đoán đúng.
- Ví dụ dự đoán sai.
- Nhận xét giả thuyết:
  - K-means có giúp không?
  - Shape features có giúp không?
  - Lớp nào khó nhất?
  - Hạn chế của pipeline là gì?

