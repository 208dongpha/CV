# Báo cáo tóm tắt đồ án: 
### Thực nghiệm đánh giá và so sánh hiệu quả các pipeline xử lý ảnh cho phân loại rác trên bộ dữ liệu TrashNet



## Tóm tắt tài liệu TrashNet

TrashNet là một bộ dữ liệu ảnh rác được giới thiệu bởi Gary Thung và Mindy Yang trong dự án phân loại rác theo khả năng tái chế. Bộ dữ liệu gồm 2527 ảnh thuộc 6 lớp: `glass`, `paper`, `cardboard`, `plastic`, `metal` và `trash`. Các ảnh trong TrashNet thường là ảnh một vật thể rác chính, được chụp tương đối rõ, vật thể thường nằm gần trung tâm khung hình.

Mục tiêu ban đầu của TrashNet là xây dựng một hệ thống có thể nhận dạng loại rác từ ảnh, từ đó hỗ trợ phân loại rác tái chế. Trong tài liệu/dự án gốc, các tác giả sử dụng TrashNet như một benchmark cho bài toán garbage image classification và có thử nghiệm với các mô hình học máy/học sâu. Kết quả CNN trong dự án gốc được xem là một mốc tham khảo quan trọng, nhưng không phải là mốc so sánh tuyệt đối cho đồ án này vì cách chia dữ liệu, tiền xử lý, mô hình và điều kiện huấn luyện có thể khác nhau.

Trong đồ án này, TrashNet được dùng làm dữ liệu thực nghiệm chính vì có số lớp rõ ràng, dung lượng vừa phải, phù hợp để chạy trên máy cá nhân và đủ gần với bài toán thực tế phân loại rác. Nhóm không dùng TrashNet để chứng minh mô hình vượt các nghiên cứu deep learning, mà dùng để so sánh công bằng các pipeline xử lý ảnh cổ điển trên cùng một tập dữ liệu. Cụ thể, nhóm kiểm tra xem các bước như K-means segmentation, contour crop, HOG, shape features, HSV histogram và SVM ảnh hưởng như thế nào đến kết quả phân loại.

Từ bối cảnh TrashNet, bài toán trong đồ án được hiểu là: với ảnh đầu vào là một vật thể rác, hệ thống cần dự đoán ảnh thuộc lớp nào trong 6 lớp rác. Kết quả được đánh giá bằng accuracy, macro-F1, weighted-F1, classification report và confusion matrix. Ngoài ra, vì yêu cầu học phần nhấn mạnh pipeline xử lý ảnh, notebook còn trình bày ảnh trung gian sau từng bước xử lý và parameter sweep cho các thuật toán chính.

## 1. Mục tiêu đề tài

Đề tài giải quyết bài toán phân loại hình ảnh rác trên bộ dữ liệu TrashNet gồm 6 lớp:

- `cardboard`
- `glass`
- `metal`
- `paper`
- `plastic`
- `trash`

Mục tiêu chính không chỉ là tạo một mô hình dự đoán nhãn rác, mà là đánh giá có hệ thống các bước xử lý ảnh trong pipeline phân loại rác:

- Resize và tiền xử lý ảnh.
- K-means segmentation.
- Morphology.
- Contour crop.
- HOG feature.
- Shape features.
- HSV color histogram.
- SVM classifier.

## 2. Giả thuyết và tiêu chí thành công

Giả thuyết chính:

```text
Pipeline có K-means segmentation, contour crop và shape features sẽ cải thiện so với baseline HOG + SVM,
vì crop có thể giảm ảnh hưởng của nền và shape features bổ sung thông tin hình dạng.
```

Giả thuyết mở rộng:

```text
HOG + HSV color histogram có thể cải thiện kết quả vì màu sắc là thông tin quan trọng trong phân loại rác.
```

Tiêu chí thành công:

- Pipeline proposed có `accuracy` hoặc `macro-F1` cao hơn baseline.
- Có confusion matrix và classification report.
- Có ảnh trung gian sau từng bước xử lý.
- Có parameter sweep với ảnh/biểu đồ đầu ra.
- Code train đúng input theo pipeline đã mô tả.

## 3. Cơ sở so sánh trên bộ dữ liệu TrashNet

Đồ án này chỉ thực nghiệm và so sánh trên bộ dữ liệu TrashNet. Vì vậy, cơ sở đánh giá chính không phải là so sánh trực tiếp với nhiều dataset khác, mà là so sánh các pipeline trên cùng TrashNet, cùng cách chia train/test và cùng metric.

Các tài liệu liên quan được dùng theo vai trò sau:

1. **TrashNet gốc**: cung cấp dataset, số lớp, bối cảnh bài toán và mốc tham khảo ban đầu. TrashNet gồm 2527 ảnh thuộc 6 lớp rác: `glass`, `paper`, `cardboard`, `plastic`, `metal`, `trash`.
2. **Các nghiên cứu sử dụng TrashNet**: được dùng để hiểu rằng TrashNet là benchmark phổ biến cho garbage image classification và để biết các hướng mạnh hơn như CNN/transfer learning có thể đạt kết quả cao hơn. Tuy nhiên, các kết quả đó chỉ là bối cảnh tham khảo vì cách chia dữ liệu, augmentation, kiến trúc mô hình và điều kiện huấn luyện có thể khác nhau.
3. **HOG và SVM**: là cơ sở thuật toán cho pipeline xử lý ảnh cổ điển của nhóm.

Trong đồ án, kết luận về hiệu quả mô hình dựa trên so sánh nội bộ giữa các pipeline sau trên cùng TrashNet:

- Baseline 1: `Resize -> HOG -> SVM`.
- Baseline 2: `Resize -> HOG + Shape -> SVM`.
- Proposed 1: `K-means crop -> HOG -> SVM`.
- Proposed 2: `K-means crop -> HOG + Shape -> SVM`.
- Extension: `HOG + HSV -> SVM`.
- Optimized: `HOG(6) + HSV(32) -> SVM`.

Vì vậy, khi nhắc đến tài liệu TrashNet, nhóm không kết luận mô hình của mình tốt hơn hoặc kém hơn tuyệt đối so với mô hình trong tài liệu. Nhóm dùng TrashNet làm bối cảnh và dùng kết quả nội bộ trên cùng dataset để đánh giá pipeline nào hiệu quả hơn trong phạm vi đồ án.

Nguồn tham khảo chính:

- TrashNet: https://github.com/garythung/trashnet
- Recyclable Waste Identification Using CNN Image Recognition and Gaussian Clustering: https://arxiv.org/abs/2011.01353
- HOG: Dalal and Triggs, CVPR 2005.
- SVM: Cortes and Vapnik, Machine Learning 1995.

## 4. Cấu trúc thư mục

```text
lab/
  lab.ipynb
  description.md
  README.md
  requirements.txt
  data/
    raw/
    trashnet_resized/
  models/
    best_garbage_classifier.joblib
    model_metadata.joblib
```

Lưu ý:

- Thư mục `data/` và `models/` không nên push lên GitHub vì có dữ liệu/model sinh ra khi chạy.
- Dataset sẽ được tải lại tự động trong notebook.

## 5. Cài đặt và chạy

Trong PowerShell:

```powershell
cd D:\Dongphh\CVision\lab
..\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Nếu môi trường ảo nằm trong thư mục `lab` thì dùng:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Mở notebook:

```powershell
jupyter notebook lab.ipynb
```

Sau đó chạy:

```text
Kernel -> Restart Kernel and Run All
```

## 6. Dataset

Notebook dùng TrashNet bản resized từ Hugging Face/GitHub.

Kết quả đọc dữ liệu:

```text
Tổng số ảnh: 2527

paper        594
glass        501
plastic      482
metal        410
cardboard    403
trash        137
```

Nhận xét:

- Dataset có 6 lớp đúng với bài toán.
- Dữ liệu bị lệch lớp, đặc biệt lớp `trash` ít nhất.
- Vì dữ liệu lệch lớp nên bài dùng thêm `macro-F1`, `weighted-F1`, classification report và confusion matrix, không chỉ nhìn accuracy.

## 7. Các bước xử lý ảnh có output trung gian

Notebook có ảnh/biểu đồ cho từng bước:

1. Ảnh gốc.
2. Ảnh resize `128x128`.
3. Ảnh grayscale.
4. Gaussian blur.
5. K-means mask.
6. Mask sau morphology.
7. Contour + bounding box.
8. Ảnh sau crop.
9. HOG visualization.
10. HSV histogram.
11. Shape mask và contour dùng để tính shape features.

Nhận xét:

- Ảnh TrashNet thường đã được chụp với vật thể nằm giữa khung hình.
- Vì vậy ảnh sau crop trong nhiều trường hợp không khác ảnh resize quá nhiều.
- Điều này giải thích vì sao K-means crop chỉ cải thiện nhẹ so với baseline.


## 8. Lý do lựa chọn thuật toán trong từng bước xử lý

Phần này giải thích ý nghĩa của từng thuật toán trong pipeline và lý do nhóm chọn thuật toán đó thay vì các lựa chọn khác. Mục tiêu là bảo đảm pipeline không chỉ chạy được mà còn có cơ sở thiết kế rõ ràng.

### 8.1. Resize ảnh về 128x128

**Ý nghĩa:** Resize giúp tất cả ảnh có cùng kích thước đầu vào. Điều này cần thiết vì các đặc trưng như HOG, HSV histogram và shape features phải tạo ra vector có số chiều cố định để đưa vào SVM.

**Lý do chọn:** Kích thước `128x128` đủ nhỏ để chạy nhanh trên máy cá nhân, nhưng vẫn giữ được hình dạng tổng thể của vật thể rác. Đây là lựa chọn cân bằng giữa độ chi tiết ảnh và thời gian tính toán.

**Không dùng ảnh gốc vì:** ảnh gốc có kích thước lớn hơn, làm thời gian trích xuất HOG tăng và có thể gây khó khăn khi so sánh giữa các pipeline. Kích thước lớn hơn như `224x224` hoặc `256x256` có thể giữ nhiều chi tiết hơn, nhưng làm vector đặc trưng dài hơn và thời gian huấn luyện tăng đáng kể.

### 8.2. Grayscale và Gaussian blur

**Ý nghĩa:** Grayscale được dùng trước HOG vì HOG mô tả hướng gradient/cạnh, chủ yếu dựa trên thay đổi cường độ sáng. Gaussian blur được dùng trong phần minh họa tiền xử lý và một số bước mask/contour để giảm nhiễu nhỏ.

**Lý do chọn:** Grayscale giúp tập trung vào hình dạng và biên vật thể. Gaussian blur giúp ảnh mượt hơn, hạn chế các cạnh nhiễu nhỏ trước khi threshold hoặc tìm contour.

**Không chỉ dùng grayscale vì:** grayscale làm mất thông tin màu. Do đó nhóm bổ sung pipeline mở rộng HOG + HSV để kiểm tra vai trò của màu sắc trong bài toán phân loại rác.

### 8.3. HOG feature

**Ý nghĩa:** HOG, tức Histogram of Oriented Gradients, mô tả hướng cạnh và hình dạng của vật thể. Với ảnh rác, hình dạng và biên của chai nhựa, giấy, bìa carton, lon kim loại hoặc thủy tinh là thông tin quan trọng.

**Lý do chọn:** HOG là đặc trưng ảnh cổ điển, dễ giải thích, có thể hiển thị bằng HOG visualization và phù hợp với yêu cầu học phần vì cho thấy rõ quá trình trích xuất đặc trưng từ ảnh.

**Không dùng CNN làm mô hình chính vì:** CNN có thể đạt độ chính xác cao hơn nhưng khó giải thích từng bước xử lý ảnh hơn. Mục tiêu của đồ án là đánh giá pipeline xử lý ảnh cổ điển có ảnh trung gian, parameter sweep và phân tích rõ từng bước. CNN phù hợp hơn như hướng mở rộng sau này.

### 8.4. SVM classifier

**Ý nghĩa:** SVM nhận vector đặc trưng từ HOG, HSV hoặc shape features và học ranh giới phân loại giữa các lớp rác.

**Lý do chọn:** SVM phù hợp với dataset vừa phải như TrashNet và vector đặc trưng thủ công có số chiều cao. Kết quả tuning cho thấy SVM kernel RBF với `C=10`, `gamma=scale` cải thiện rõ so với linear SVM.

**Không chọn KNN vì:** KNN dự đoán chậm hơn do phải so sánh ảnh mới với nhiều mẫu train, đồng thời dễ bị ảnh hưởng bởi nhiễu trong không gian đặc trưng cao.

**Không chọn Random Forest làm chính vì:** Random Forest dễ dùng nhưng thường không tối ưu bằng SVM đối với đặc trưng HOG/HSV liên tục và số chiều lớn.

### 8.5. K-means segmentation

**Ý nghĩa:** K-means phân cụm màu của pixel để ước lượng vùng foreground/background, từ đó hỗ trợ crop vật thể chính.

**Lý do chọn:** TrashNet chỉ có nhãn lớp, không có ground truth mask. Vì vậy K-means là lựa chọn phù hợp vì không cần annotation pixel-level. Thuật toán này cũng thuộc nhóm phân đoạn ảnh, đúng với nội dung học phần.

**Không dùng threshold cố định vì:** ảnh có độ sáng, nền và màu vật thể khác nhau. Một ngưỡng cố định có thể đúng với ảnh này nhưng sai với ảnh khác.

**Không dùng Mask R-CNN hoặc mô hình segmentation học sâu vì:** các mô hình này cần pretrained model hoặc dữ liệu segmentation phức tạp hơn. Trong phạm vi đồ án, nhóm cần một phương pháp có thể giải thích và chạy trực tiếp trên dữ liệu hiện có.

### 8.6. Morphology

**Ý nghĩa:** Morphology được dùng để làm sạch mask sau K-means. Opening giúp loại bỏ nhiễu nhỏ, closing giúp lấp lỗ trong vùng foreground.

**Lý do chọn:** Mask sau K-means thường chưa sạch hoàn toàn. Nếu đưa mask nhiễu trực tiếp vào contour detection, contour có thể bị vỡ hoặc bounding box không ổn định.

**Không bỏ morphology vì:** bỏ bước này làm contour dễ sai, kéo theo shape features như area, perimeter, solidity và circularity bị nhiễu.

### 8.7. Contour crop

**Ý nghĩa:** Contour giúp xác định vùng vật thể chính sau segmentation. Bounding box từ contour được dùng để crop vật thể, giảm ảnh hưởng của nền.

**Lý do chọn:** Crop giúp HOG và shape features tập trung vào vật thể thay vì toàn ảnh. Đây là bước quan trọng trong Proposed 1 và Proposed 2.

**Nhận xét thực nghiệm:** Trên TrashNet, vật thể thường nằm giữa ảnh và nền tương đối sạch nên crop chỉ cải thiện nhẹ. Điều này giải thích vì sao Proposed 2 tốt nhất trong 4 pipeline chính nhưng chưa vượt pipeline HOG + HSV.

### 8.8. Shape features

**Ý nghĩa:** Shape features gồm area ratio, perimeter ratio, aspect ratio, extent, solidity, circularity và Hu moments. Các đặc trưng này mô tả hình dạng tổng thể của vật thể.

**Lý do chọn:** Shape features bổ sung thông tin hình học mà HOG có thể chưa mô tả đầy đủ. Nhóm dùng chúng để kiểm tra liệu thông tin contour có cải thiện phân loại hay không.

**Nhận xét thực nghiệm:** Shape features chưa cải thiện khi dùng trực tiếp trên ảnh gốc, nhưng sau K-means crop thì Proposed 2 tốt hơn Proposed 1 một chút. Điều này cho thấy shape features chỉ hữu ích khi contour tương đối ổn định.

### 8.9. HSV color histogram

**Ý nghĩa:** HSV histogram mô tả phân bố màu sắc của ảnh theo Hue, Saturation và Value. Đây là thông tin HOG grayscale không có.

**Lý do chọn:** Trong phân loại rác, màu sắc rất quan trọng. Ví dụ paper thường sáng, cardboard có màu nâu/vàng, glass có vùng phản chiếu, plastic có màu đa dạng và metal có độ sáng đặc trưng.

**Không chỉ dùng RGB histogram vì:** RGB trộn thông tin màu với độ sáng, dễ bị ảnh hưởng bởi điều kiện chiếu sáng. HSV tách sắc độ, độ bão hòa và độ sáng rõ hơn nên phù hợp hơn cho histogram màu.

**Nhận xét thực nghiệm:** HOG + HSV cải thiện rõ so với HOG đơn thuần. Sau khi tối ưu tham số, `Optimized HOG(6) + HSV(32) + SVM` đạt kết quả cao nhất toàn bộ thí nghiệm.

### 8.10. Parameter sweep

**Ý nghĩa:** Parameter sweep giúp kiểm tra ảnh hưởng của tham số đến ảnh trung gian và metric, tránh chọn tham số tùy ý.

**Các tham số đã khảo sát:**

- K-means: `k = 2, 3, 4`.
- HOG: `orientations = 6, 9, 12`.
- HSV: `bins = 8, 16, 32`.
- SVM: `kernel = linear/rbf`, `C = 0.1, 1, 10`.

**Ý nghĩa thực nghiệm:** Sau sweep, nhóm train lại mô hình với tham số tốt nhất thay vì chỉ dừng ở bảng kết quả. Mô hình optimized đạt accuracy cao hơn HOG + HSV mặc định, chứng minh parameter sweep có tác dụng thực tế.

## 9. Bốn pipeline chính

### Baseline 1

```text
Ảnh gốc -> Resize -> HOG -> SVM
```

Mục đích:

- Làm mốc cơ bản.
- Kiểm tra HOG + SVM khi chưa segmentation.

### Baseline 2

```text
Ảnh gốc -> Resize -> HOG + Shape features -> SVM
```

Mục đích:

- Kiểm tra shape features khi chưa crop vật thể.

### Proposed 1

```text
Ảnh gốc -> K-means segmentation -> contour crop -> HOG -> SVM
```

Mục đích:

- Kiểm tra tác dụng của segmentation/crop.

### Proposed 2

```text
Ảnh gốc -> K-means segmentation -> contour crop -> HOG + Shape features -> SVM
```

Mục đích:

- Pipeline chính trong 4 pipeline theo đề tài.
- Kiểm tra segmentation + shape features có cải thiện baseline không.

## 10. Pipeline mở rộng

```text
Ảnh gốc -> Resize -> HOG + HSV color histogram -> SVM
```

Lý do thêm HSV:

- HOG dùng grayscale nên mất thông tin màu.
- Với phân loại rác, màu sắc rất quan trọng:
  - `paper` thường sáng.
  - `cardboard` thường nâu/vàng.
  - `glass` có phản chiếu/sáng.
  - `plastic` có màu đa dạng.
  - `metal` có độ sáng và phản xạ riêng.

Sau parameter sweep, notebook train lại mô hình tối ưu:

```text
Optimized HOG(6) + HSV(32) + SVM
```

## 11. Kết quả chính

| Pipeline | Accuracy | Macro-F1 | Nhận xét |
|---|---:|---:|---|
| Baseline 1: HOG + SVM | 58.70% | 0.5962 | Baseline cơ bản |
| Baseline 2: HOG + Shape + SVM | 58.50% | 0.5959 | Shape features chưa cải thiện khi chưa crop |
| Proposed 1: K-means crop + HOG + SVM | 60.28% | 0.5911 | Crop giúp tăng accuracy nhẹ |
| Proposed 2: K-means crop + HOG + Shape + SVM | 60.87% | 0.5965 | Tốt nhất trong 4 pipeline chính |
| Tuned HOG + SVM | 65.42% | 0.6472 | Tuning SVM cải thiện rõ |
| HOG + HSV + SVM | 67.79% | 0.6671 | Mở rộng màu sắc, tốt hơn HOG |
| Optimized HOG(6) + HSV(32) + SVM | 68.77% | 0.6755 | Tốt nhất toàn bộ thí nghiệm |

## 12. Nhận xét kết quả

Trong 4 pipeline chính, `Proposed 2` là tốt nhất:

```text
Proposed 2 accuracy = 60.87%
Baseline 1 accuracy = 58.70%
```

Điều này cho thấy K-means crop và shape features có cải thiện baseline, nhưng mức cải thiện không lớn.

Nguyên nhân:

- TrashNet resized thường có vật thể nằm giữa ảnh.
- Nền ảnh tương đối sạch.
- Crop không làm thay đổi ảnh quá nhiều.
- Shape features phụ thuộc vào chất lượng mask/contour, nên nếu contour chưa ổn định thì đặc trưng có thể bị nhiễu.

Pipeline mở rộng `HOG + HSV + SVM` tốt hơn các pipeline dùng crop:

```text
HOG + HSV + SVM accuracy = 67.79%
Optimized HOG(6) + HSV(32) + SVM accuracy = 68.77%
```

Điều này chứng minh màu sắc là đặc trưng quan trọng trong phân loại rác.

## 13. Parameter sweep

Notebook có parameter sweep kèm output ảnh/biểu đồ:

### K-means

```text
k = 2, 3, 4
```

Output:

- Mask.
- Contour + bounding box.
- Ảnh crop.
- Crop rate.

Kết quả crop rate trên tập con:

| k | Crop rate |
|---:|---:|
| 2 | 97.50% |
| 3 | 93.33% |
| 4 | 79.17% |

Nhận xét:

- `k=2` crop rate cao nhưng không chắc mask trực quan tốt hơn.
- `k=4` dễ làm mask phân mảnh hơn.
- `k=3` được dùng trong pipeline chính như lựa chọn cân bằng.

### HOG

```text
orientations = 6, 9, 12
```

Output:

- HOG visualization.
- Validation accuracy.
- Validation macro-F1.

Kết quả trên tập con:

| Orientations | Feature dim | Validation accuracy | Validation macro-F1 |
|---:|---:|---:|---:|
| 6 | 5400 | 57.30% | 0.5687 |
| 9 | 8100 | 54.49% | 0.5416 |
| 12 | 10800 | 57.30% | 0.5669 |

Nhận xét:

- `orientations=6` tốt nhất trên tập con.
- Vì vậy notebook train lại mô hình optimized với HOG orientation = 6.

### HSV

```text
bins = 8, 16, 32
```

Output:

- Biểu đồ HSV histogram.
- Validation accuracy.
- Validation macro-F1.

Kết quả trên tập con:

| Bins/channel | Feature dim | Validation accuracy | Validation macro-F1 |
|---:|---:|---:|---:|
| 8 | 8124 | 55.06% | 0.5470 |
| 16 | 8148 | 56.18% | 0.5585 |
| 32 | 8196 | 56.74% | 0.5645 |

Nhận xét:

- `bins=32` tốt nhất trên tập con.
- Notebook train lại mô hình optimized với HSV bins = 32.

### SVM

Tham số thử:

```text
kernel = linear/rbf
C = 0.1, 1, 10
```

Kết quả tốt nhất:

```text
kernel = rbf
C = 10
gamma = scale
```

Nhận xét:

- RBF tốt hơn linear, chứng tỏ ranh giới giữa các lớp rác không hoàn toàn tuyến tính.
- Tuning SVM tăng accuracy từ 58.70% lên 65.42%.

## 14. Train lại mô hình với tham số tốt nhất

Sau parameter sweep, notebook không dừng ở bảng kết quả mà train lại full model với tham số tốt nhất:

```text
HOG orientations = 6
HSV bins = 32
SVM kernel = rbf
C = 10
gamma = scale
```

Kết quả:

```text
Optimized HOG(6) + HSV(32) + SVM
Accuracy = 68.77%
Macro-F1 = 0.6755
Weighted-F1 = 0.6860
```

So với HOG + HSV mặc định:

```text
HOG + HSV mặc định: 67.79%
Optimized HOG + HSV: 68.77%
```

Kết luận:

- Parameter sweep có tác dụng thực tế.
- Cấu hình optimized vừa chính xác hơn vừa có số chiều đặc trưng thấp hơn:

```text
HOG + HSV mặc định feature dim = 8148
Optimized feature dim = 5496
```

## 15. Kiểm tra pipeline-code nhất quán

Notebook có bảng audit cuối bài để kiểm tra input đưa vào mô hình.

| Pipeline | Input đưa vào model | Đúng mô tả |
|---|---|---|
| Baseline 1 | Ảnh gốc sau resize 128x128 | Có |
| Baseline 2 | Ảnh gốc sau resize 128x128 | Có |
| Proposed 1 | Ảnh sau K-means crop, rồi resize 128x128 | Có |
| Proposed 2 | Ảnh sau K-means crop, rồi resize 128x128 | Có |
| Extension/Demo | Ảnh gốc resize + HOG/HSV optimized | Có |

Điểm quan trọng:

```text
Proposed 1 và Proposed 2 thật sự gọi kmeans_crop_foreground() trước khi trích đặc trưng.
Không có lỗi mô tả crop nhưng code lại train bằng ảnh gốc.
```

## 16. Demo dự đoán

Notebook có hai phần demo:

1. Dự đoán một ảnh test bất kỳ.
2. Dự đoán 10 ảnh ngẫu nhiên trong tập test.

Kết quả demo 10 ảnh:

```text
Số ảnh dự đoán đúng: 8/10
```

Nhận xét:

- Kết quả 8/10 phù hợp với accuracy test khoảng 68-69%.
- Các lỗi dự đoán có thể dùng để phân tích trong phần thảo luận.
- Một số lớp dễ nhầm: `plastic`, `paper`, `metal`, `cardboard`.

## 17. Kết luận

Giả thuyết chính đúng một phần:

```text
K-means crop + shape features có cải thiện baseline, nhưng mức cải thiện không lớn.
```

Giả thuyết mở rộng đúng rõ hơn:

```text
Bổ sung HSV color histogram giúp cải thiện đáng kể vì màu sắc là đặc trưng quan trọng trong phân loại rác.
```

Mô hình tốt nhất:

```text
Optimized HOG(6) + HSV(32) + SVM
Accuracy = 68.77%
Macro-F1 = 0.6755
```

Mô hình dùng cho demo:

```text
Optimized HOG(6) + HSV(32) + SVM
```

Hướng cải thiện:

- Thử thêm color space khác như Lab.
- Sweep thêm morphology kernel và contour min area.
- Cân bằng dữ liệu cho lớp `trash`.
- Dùng data augmentation.
- So sánh thêm với CNN/transfer learning như một hướng nâng cao.
