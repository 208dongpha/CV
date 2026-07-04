# TOPIC

Xây dựng và đánh giá hiệu quả các thuật toán trong bài toán phân loại hình ảnh rác tái chế.

# Purpose/Goal

## Tóm tắt định hướng nghiên cứu

Đề tài này được định hướng như một bài toán thực nghiệm đánh giá pipeline, không chỉ là một ứng dụng dự đoán nhãn đơn lẻ. Trọng tâm của dự án là **thực nghiệm và đánh giá**: trong bài toán phân loại rác tái chế, nhóm kiểm tra xem các bước xử lý ảnh cổ điển như K-means segmentation, contour crop và shape features có cải thiện kết quả phân loại so với baseline hay không.

Nói ngắn gọn, câu hỏi chính của project là:

```text
Nếu cùng dùng HOG + SVM để phân loại rác, việc thêm K-means segmentation
và contour/shape features có làm accuracy hoặc macro-F1 tốt hơn không?
```

Project sẽ có baseline, proposed method, parameter sweep và metric rõ ràng:

```text
Baseline 1:
Ảnh gốc -> Resize -> HOG -> SVM

Baseline 2:
Ảnh gốc -> Resize -> HOG + shape features -> SVM

Proposed 1:
Ảnh gốc -> K-means segmentation -> contour crop -> HOG -> SVM

Proposed 2:
Ảnh gốc -> K-means segmentation -> contour crop -> HOG + shape features -> SVM
```

Các tham số sẽ được kiểm chứng:

- K-means: số cụm `k = 2, 3, 4, 5`, không gian màu `RGB`, `HSV`, `Lab`.
- Morphology: kernel `3x3`, `5x5`, `7x7`.
- Contour: min area `100`, `500`, `1000` pixel.
- HOG: orientations `6`, `9`, `12`; pixels per cell `(8,8)`, `(16,16)`.
- SVM: `C = 0.1`, `1`, `10`; kernel `linear`, `rbf`.

Metric đánh giá:

- Accuracy.
- Macro precision, macro recall, macro F1-score.
- Per-class F1-score.
- Confusion matrix.
- Ảnh trung gian của từng bước pipeline.

Mục tiêu của dự án không chỉ là tạo một mô hình dự đoán nhãn rác, mà là **đánh giá có hệ thống ảnh hưởng của các bước xử lý ảnh trong pipeline phân loại rác tái chế**. Cụ thể, nhóm sẽ so sánh pipeline phân loại trực tiếp từ ảnh gốc với pipeline có thêm K-means segmentation, contour crop và shape features để kiểm tra xem các kỹ thuật trong môn học có thật sự cải thiện kết quả phân loại hay không.

Các lớp rác dự kiến gồm: `plastic`, `paper`, `cardboard`, `glass`, `metal` và `trash/organic`. Bài toán có ý nghĩa thực tế trong hệ thống thùng rác thông minh, dây chuyền phân loại rác tự động và ứng dụng hướng dẫn người dùng phân loại rác bằng ảnh chụp từ điện thoại.

## Define Problem

Bài toán được định nghĩa như sau:

```text
Input:
  Một ảnh RGB chứa một vật thể rác chính.

Output:
  Nhãn loại rác của ảnh, ví dụ plastic/paper/cardboard/glass/metal/trash.

Nhiệm vụ:
  Thiết kế và đánh giá pipeline xử lý ảnh để phân loại đúng loại rác.
```

Khó khăn chính của bài toán:

- Nền ảnh có thể phức tạp, không đồng nhất.
- Ánh sáng thay đổi làm màu vật thể bị lệch.
- Một số lớp dễ nhầm nhau, ví dụ `paper` và `cardboard`, hoặc `plastic` và `glass`.
- Hình dạng vật thể trong cùng một lớp rất đa dạng.
- Dataset có thể lệch lớp, nên accuracy tổng thể chưa đủ; cần thêm macro-F1 và confusion matrix.

Do đó, câu hỏi nghiên cứu của dự án là:

```text
K-means segmentation và contour/shape features có cải thiện hiệu quả của HOG+SVM
trong bài toán phân loại rác tái chế so với baseline phân loại trực tiếp trên ảnh gốc không?
```

## Cơ sở tài liệu

Dự án dựa trên các nguồn dữ liệu và nghiên cứu liên quan đến garbage/waste image classification:

- **TrashNet**: dataset rác 6 lớp gồm `glass`, `paper`, `cardboard`, `plastic`, `metal`, `trash`, tổng 2527 ảnh. Đây là dataset phổ biến cho bài toán garbage image classification và có baseline CNN khoảng 75% test accuracy theo mô tả của tác giả. Link: https://github.com/garythung/trashnet
- **TACO - Trash Annotations in Context**: dataset rác trong ngữ cảnh thật, có annotation cho detection/segmentation. Nguồn này cho thấy bài toán rác ngoài thực tế khó hơn ảnh crop đơn giản vì nền phức tạp, vật thể nhỏ và bị che khuất. Link: https://arxiv.org/abs/2003.06975
- **HGI-30 - Household Garbage Image Recognition**: benchmark ảnh rác gia đình với nhiều lớp hơn, nhấn mạnh các khó khăn như ánh sáng, nền phức tạp và hình dạng đa dạng. Link: https://arxiv.org/abs/2202.11878
- **Garbage Dataset (GD)**: benchmark multi-class cho automated waste segregation, dùng để tham khảo cách đánh giá bằng accuracy, per-class metric và confusion matrix. Link: https://arxiv.org/abs/2602.10500

Các nguồn này cho thấy bài toán phân loại rác là một bài toán thực tế có dataset, baseline và metric rõ ràng. Vì vậy project không dừng ở mức demo upload ảnh, mà tập trung vào so sánh thuật toán và phân tích điều kiện nào làm pipeline hoạt động tốt hoặc thất bại.

## Giả thuyết kiểm chứng

Pipeline có bước K-means segmentation và contour crop trước khi phân loại sẽ cho kết quả tốt hơn pipeline phân loại trực tiếp trên ảnh gốc, vì phân cụm màu và contour giúp giảm ảnh hưởng của nền, ánh sáng, vật thể phụ và bố cục ảnh không đồng nhất. Ngoài ra, shape features trích từ contour có thể bổ sung thông tin hình dạng cho HOG, giúp SVM phân biệt tốt hơn các lớp có hình dạng đặc trưng.

## Tiêu chí thành công

- Proposed pipeline đạt `accuracy` hoặc `macro-F1` cao hơn baseline trực tiếp trên ảnh gốc.
- Confusion matrix cho thấy một số cặp lớp dễ nhầm, ví dụ `paper/cardboard` hoặc `plastic/glass`, được cải thiện sau segmentation/crop.
- Có phân tích per-class precision, recall, F1-score thay vì chỉ báo cáo accuracy tổng thể.
- Notebook hiển thị đầy đủ ảnh trung gian: ảnh gốc, ảnh sau tiền xử lý, ảnh phân cụm K-means, mask, contour, crop vật thể và kết quả dự đoán.
- Có khảo sát tham số với ít nhất 3 giá trị cho các bước chính: số cụm K-means, kernel morphology, HOG descriptor và SVM classifier.
- Có phần thảo luận trường hợp thất bại: nền cùng màu vật thể, vật thể trong suốt, vật thể bị che khuất hoặc ảnh có nhiều vật thể.

## Pipeline chính được chọn

```text
Ảnh rác đầu vào
        |
        v
Ch.2 - Tiền xử lý ảnh
resize, Gaussian blur, CLAHE/chuẩn hóa màu
        |
        v
Ch.4 - Phân đoạn vật thể
K-means clustering + morphology
        |
        v
Ch.3 - Contour và đặc trưng hình dạng
findContours, bounding box, area, perimeter, aspect ratio, circularity
        |
        v
Ch.5 - Nhận dạng ảnh
HOG feature + SVM classifier
        |
        v
Nhãn loại rác + metric đánh giá
```

Pipeline này được chọn vì cân bằng giữa tính khả thi và yêu cầu học phần: có đủ tiền xử lý, phân đoạn, đặc trưng hình dạng và nhận dạng; đồng thời vẫn dễ giải thích, dễ khảo sát tham số và dễ đánh giá bằng các chỉ số định lượng.

## Mô hình, thuật toán và baseline đánh giá

Nhóm sẽ không chỉ huấn luyện một model duy nhất, mà so sánh nhiều cấu hình để trả lời câu hỏi “bước nào thật sự giúp cải thiện kết quả?”.

| Ký hiệu | Pipeline | Mục đích |
|---|---|---|
| Baseline 1 | Ảnh gốc -> Resize -> HOG -> SVM | Mốc cơ bản, không segmentation |
| Baseline 2 | Ảnh gốc -> Resize -> HOG + shape features -> SVM | Kiểm tra shape features khi chưa crop vật thể |
| Proposed 1 | Ảnh gốc -> K-means segmentation -> contour crop -> HOG -> SVM | Kiểm tra tác dụng của segmentation/crop |
| Proposed 2 | Ảnh gốc -> K-means segmentation -> contour crop -> HOG + shape features -> SVM | Pipeline chính của nhóm |
| Extension | Ảnh crop -> CNN transfer learning | Mốc tham khảo nếu còn thời gian |

Các tham số chính cần so sánh:

- K-means: `k = 2, 3, 4, 5`; color space: `RGB`, `HSV`, `Lab`.
- Morphology: kernel size `3x3`, `5x5`, `7x7`.
- Contour: min area `100`, `500`, `1000` pixel; có/không dùng shape features.
- HOG: orientations `6`, `9`, `12`; pixels per cell `(8,8)`, `(16,16)`.
- SVM: `C = 0.1`, `1`, `10`; kernel `linear`, `rbf`.

Metric đánh giá:

- Accuracy.
- Macro precision, macro recall, macro F1-score.
- Per-class F1-score.
- Confusion matrix.
- Thời gian dự đoán trung bình mỗi ảnh nếu cần so sánh tính thực dụng.

## Ứng dụng thực tế

Phân loại rác tái chế là một bài toán thực tế trong các hệ thống thùng rác thông minh, dây chuyền phân loại rác tự động và ứng dụng giáo dục môi trường. Camera có thể chụp ảnh vật thể rác, hệ thống xử lý ảnh tách vật thể khỏi nền, sau đó mô hình nhận dạng dự đoán loại rác để hỗ trợ quyết định bỏ vào đúng nhóm.

Một số ví dụ ứng dụng:

- **Thùng rác thông minh:** nhận dạng rác là nhựa, giấy, kim loại hay thủy tinh để hướng dẫn người dùng bỏ đúng ngăn.
- **Dây chuyền tái chế:** hỗ trợ phân loại rác tự động trước khi đưa vào quy trình xử lý.
- **Ứng dụng di động:** người dùng chụp ảnh vật thể rác và nhận gợi ý loại rác tương ứng.
- **Giáo dục môi trường:** minh họa cách thị giác máy tính có thể hỗ trợ phân loại và tái chế rác.
- **Giám sát chất lượng phân loại:** phát hiện các trường hợp bỏ sai loại rác trong khu vực công cộng hoặc trường học.

Trong phạm vi dự án cuối kỳ, nhóm tập trung vào bài toán phân loại ảnh rác đã chứa một vật thể chính. Đây là phiên bản đơn giản hơn so với hệ thống phân loại rác hoàn chỉnh trong công nghiệp, nhưng vẫn thể hiện đầy đủ vai trò của các kỹ thuật trong môn học: tiền xử lý ảnh, phân đoạn ảnh, trích xuất đặc trưng và nhận dạng ảnh.

# Input

Dữ liệu chính:

- Ảnh rác thực tế từ dataset công khai hoặc ảnh tự chụp.
- Các lớp đề xuất: `plastic`, `paper`, `cardboard`, `glass`, `metal`, `trash`.
- Dataset có thể dùng:
  - TrashNet: dataset phân loại rác phổ biến với các lớp như glass, paper, cardboard, plastic, metal, trash.
  - Kaggle Garbage Classification: nhiều phiên bản dataset phân loại rác dễ dùng trong notebook.
  - TACO: dataset ảnh rác ngoài môi trường, phù hợp nếu muốn mở rộng sang detection/segmentation.

Input của chương trình:

- Một ảnh RGB/BGR chứa vật thể rác.
- Tập train/validation/test đã chia theo nhãn lớp.
- Tham số pipeline: kích thước ảnh, phương pháp segmentation, kích thước kernel morphology, tham số HOG/SVM hoặc CNN.

# Output

Output trung gian:

- Ảnh resize.
- Ảnh grayscale hoặc ảnh màu đã chuẩn hóa.
- Mask phân đoạn vật thể rác.
- Mask sau morphology.
- Bounding box hoặc crop vùng vật thể chính.
- Vector đặc trưng HOG hoặc feature từ CNN.

Output cuối:

- Nhãn dự đoán của ảnh: `plastic`, `paper`, `cardboard`, `glass`, `metal`, `trash`, v.v.
- Độ tin cậy hoặc score dự đoán nếu model hỗ trợ.
- Bảng metric: accuracy, precision, recall, F1-score.
- Confusion matrix.
- So sánh baseline và pipeline đề xuất.
- Hình ảnh parameter sweep cho các bước chính.

# How to do / Performance Step

## 1. Chuẩn bị dữ liệu

1. Chọn dataset:
   - Ưu tiên TrashNet hoặc Kaggle Garbage Classification vì có nhãn phân loại sẵn.
   - Chỉ cần dùng subset vừa phải, ví dụ 300-1000 ảnh, để notebook chạy nhanh.
2. Chọn các lớp:
   - Bản đơn giản: `plastic`, `paper`, `glass`, `metal`.
   - Bản đầy đủ hơn: thêm `cardboard`, `trash/organic`.
3. Chia dữ liệu:
   - Train: 70%.
   - Validation: 15%.
   - Test: 15%.
4. Kiểm tra phân bố lớp:
   - Số ảnh mỗi lớp.
   - Nếu lệch lớp quá nhiều, chọn subset cân bằng hơn hoặc dùng class weight.
5. Lưu cấu trúc dữ liệu đề xuất:

```text
data/
  garbage/
    train/
      plastic/
      paper/
      glass/
      metal/
    val/
      plastic/
      paper/
      glass/
      metal/
    test/
      plastic/
      paper/
      glass/
      metal/
```

## 2. Baseline không phân đoạn

Mục đích: tạo mốc so sánh để kiểm chứng giả thuyết.

Pipeline baseline:

```text
Ảnh gốc
    |
    v
Resize về kích thước cố định
    |
    v
Trích đặc trưng HOG hoặc CNN feature
    |
    v
Classifier
    |
    v
Nhãn rác
```

Các bước:

1. Đọc ảnh bằng OpenCV/PIL.
2. Resize ảnh về kích thước cố định, ví dụ `224x224` cho CNN hoặc `128x128` cho HOG.
3. Chuẩn hóa giá trị pixel.
4. Trích đặc trưng:
   - HOG cho baseline cổ điển.
   - Hoặc CNN feature nếu dùng transfer learning.
5. Huấn luyện classifier:
   - HOG + SVM.
   - Hoặc k-NN/SVM trên feature.
6. Đánh giá trên tập test.

Output cần lưu:

- Một vài ảnh input mẫu.
- Metric baseline.
- Confusion matrix baseline.

## 3. Tiền xử lý ảnh

Mục đích: giảm nhiễu và chuẩn hóa ảnh trước khi phân đoạn/nhận dạng.

Các kỹ thuật thuộc Chương 2:

1. Resize ảnh về kích thước cố định.
2. Chuyển đổi màu nếu cần:
   - BGR/RGB sang HSV hoặc Lab.
   - Grayscale nếu dùng HOG.
3. Gaussian blur để giảm nhiễu nhẹ.
4. CLAHE hoặc histogram equalization nếu ảnh có ánh sáng không đều.
5. Chuẩn hóa pixel về `[0, 1]` hoặc theo mean/std của mô hình pretrained.

Parameter sweep đề xuất:

- Kích thước ảnh: `128x128`, `224x224`, `256x256`.
- Gaussian kernel: `3x3`, `5x5`, `7x7`.
- CLAHE clipLimit: `1.0`, `2.0`, `3.0`.

Output cần lưu:

- Ảnh gốc.
- Ảnh sau resize.
- Ảnh sau tăng tương phản hoặc blur.

## 4. Phân đoạn vật thể rác

Mục đích: tách vật thể rác khỏi nền để giảm nhiễu cho bước phân loại.

Kỹ thuật thuộc Chương 4:

### Cách chính: K-means clustering + Morphology

Pipeline:

1. Chuyển ảnh từ RGB/BGR sang không gian màu Lab hoặc HSV.
2. Mỗi pixel được biểu diễn bằng vector đặc trưng màu, ví dụ `[L, a, b]` hoặc `[H, S, V]`.
3. Chạy K-means để chia pixel thành `k` cụm màu.
4. Chọn cụm ứng viên vật thể rác:
   - ưu tiên cụm nằm gần vùng trung tâm ảnh;
   - hoặc cụm khác nền rõ nhất;
   - hoặc cụm có diện tích phù hợp, không quá nhỏ và không chiếm toàn ảnh.
5. Tạo mask nhị phân từ cụm được chọn.
6. Dùng morphology opening/closing để làm sạch mask.
7. Tìm contour lớn nhất.
8. Crop vùng vật thể chính từ bounding box của contour.

Parameter sweep:

- Số cụm K-means `k`: `2`, `3`, `4`, `5`.
- Không gian màu: `RGB`, `HSV`, `Lab`.
- Morphology kernel: `3x3`, `5x5`, `7x7`.


## 5. Contour và đặc trưng hình dạng

Mục đích: liên kết bước phân đoạn với bước nhận dạng bằng cách xác định vùng vật thể chính và trích xuất các đặc trưng hình dạng từ mask.

Kỹ thuật thuộc Chương 3:

1. Sau khi có mask nhị phân từ K-means/HSV, dùng `cv2.findContours` để tìm các contour.
2. Chọn contour có diện tích lớn nhất làm vật thể rác chính.
3. Tính bounding box của contour để crop vật thể từ ảnh gốc.
4. Trích xuất shape features:
   - `area`: diện tích contour.
   - `perimeter`: chu vi contour.
   - `aspect_ratio`: tỉ lệ rộng/cao của bounding box.
   - `extent`: tỉ lệ diện tích contour trên diện tích bounding box.
   - `solidity`: tỉ lệ diện tích contour trên diện tích convex hull.
   - `circularity`: độ tròn, tính bằng `4π * area / perimeter^2`.

Lý do chọn contour:

- Sau segmentation, contour là cách tự nhiên để xác định vật thể chính.
- Bounding box từ contour giúp crop ảnh trước khi đưa vào classifier.
- Shape features bổ sung thông tin hình dạng cho HOG, ví dụ chai nhựa thường dài, lon kim loại tương đối tròn/trụ, giấy hoặc cardboard thường có dạng phẳng/chữ nhật.

Pipeline contour:

```text
Segmentation mask
        |
        v
Morphology cleaning
        |
        v
Find contours
        |
        v
Select largest contour
        |
        v
Bounding box + crop object
        |
        v
Shape features
area, perimeter, aspect ratio, circularity, extent, solidity
```

Parameter sweep đề xuất:

- Ngưỡng diện tích contour tối thiểu: `100`, `500`, `1000` pixel.
- Kernel morphology trước khi tìm contour: `3x3`, `5x5`, `7x7`.
- So sánh HOG+SVM không dùng shape features và HOG+SVM có ghép shape features.

Output cần lưu:

- Mask sau morphology.
- Ảnh có vẽ contour lớn nhất.
- Bounding box/crop vật thể.
- Bảng shape features của một vài ảnh mẫu.

## 6. Trích xuất đặc trưng

Kỹ thuật thuộc Chương 3/5:

### HOG Feature

Pipeline:

1. Chuyển ảnh crop sang grayscale.
2. Resize về kích thước cố định.
3. Tính gradient.
4. Chia ảnh thành cell.
5. Tính histogram hướng gradient.
6. Chuẩn hóa theo block.
7. Nối thành vector HOG.

Parameter sweep:

- `pixels_per_cell`: `(8,8)`, `(16,16)`, `(32,32)`.
- `cells_per_block`: `(2,2)`, `(3,3)`.
- `orientations`: `6`, `9`, `12`.

### CNN Feature / Transfer Learning

Pipeline:

1. Resize ảnh crop về `224x224`.
2. Dùng pretrained backbone như MobileNetV2, ResNet18/ResNet50.
3. Thay classifier head theo số lớp rác.
4. Có thể chọn:
   - Feature extraction: đóng băng backbone.
   - Fine-tuning: train thêm một vài layer cuối.

Parameter sweep:

- Learning rate: `1e-3`, `1e-4`, `1e-5`.
- Batch size: `16`, `32`, `64`.
- Số epoch: `5`, `10`, `15`.

## 7. Nhận dạng / Phân loại

Kỹ thuật thuộc Chương 5:

### Baseline 1: HOG + SVM

Pipeline:

```text
Ảnh crop
    |
    v
HOG descriptor
    |
    v
SVM classifier
    |
    v
Nhãn rác
```

Parameter sweep:

- SVM `C`: `0.1`, `1`, `10`.
- Kernel: `linear`, `rbf`.

## 8. Đánh giá định lượng

Metric chính:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- Confusion matrix.

Nếu có segmentation ground truth:

- IoU giữa mask dự đoán và mask thật.
- Pixel precision/recall.

Nếu không có segmentation ground truth:

- Chỉ dùng segmentation như bước tiền xử lý.
- Đánh giá gián tiếp bằng việc so sánh classification metric trước/sau segmentation.

Cách trình bày:

1. Bảng metric baseline.
2. Bảng metric proposed.
3. Confusion matrix.
4. Ví dụ ảnh dự đoán đúng.
5. Ví dụ ảnh dự đoán sai.
6. Nhận xét lớp nào dễ nhầm:
   - paper vs cardboard.
   - plastic vs glass trong ảnh trong suốt.
   - metal vs plastic nếu ánh sáng phản chiếu mạnh.

## 9. Parameter Sweep

Theo yêu cầu lab_CK, mỗi kỹ thuật chính nên có khảo sát tham số ít nhất 3 giá trị.

Gợi ý sweep:

1. K-means segmentation:
   - số cụm `k`: `2`, `3`, `4`, `5`.
   - không gian màu: `RGB`, `HSV`, `Lab`.
   - So sánh mask/crop và classification accuracy sau phân cụm.

2. Morphology:
   - kernel size: `3x3`, `5x5`, `7x7`.
   - So sánh mask có bị mất vật thể hoặc còn nhiễu nền không.

3. HOG:
   - orientations: `6`, `9`, `12`.
   - So sánh accuracy/F1 của SVM.

4. Shape features:
   - Không dùng shape features.
   - Dùng shape features thô.
   - Dùng shape features đã chuẩn hóa bằng `StandardScaler`.

5. SVM:
   - `C`: `0.1`, `1`, `10`.
   - So sánh validation accuracy.

6. CNN:
   - learning rate: `1e-3`, `1e-4`, `1e-5`.
   - So sánh validation loss/accuracy.

## 10. Baseline và Proposed

Baseline A:

```text
Ảnh gốc -> Resize -> HOG -> SVM
```

Baseline B:

```text
Ảnh gốc -> Resize -> HOG + shape features -> SVM
```

Proposed A:

```text
Ảnh gốc -> K-means segmentation -> Contour -> Crop -> HOG -> SVM
```

Proposed B:

```text
Ảnh gốc -> K-means segmentation -> Contour -> Crop -> HOG + shape features -> SVM
```

Mục tiêu so sánh:

- Segmentation có giúp classifier tốt hơn không?
- Shape features có cải thiện HOG + SVM không?
- Lớp nào vẫn bị nhầm nhiều và vì sao?

CNN transfer learning có thể được làm như phần mở rộng nếu còn thời gian, nhưng pipeline chính nên là K-means segmentation + contour + HOG/shape features + SVM để dễ giải thích theo đúng nội dung các chương.

## 11. Cấu trúc notebook/báo cáo

Notebook nên có các mục:

1. Problem statement và hypothesis.
2. Dataset và cách chọn subset.
3. Data exploration:
   - số lượng ảnh mỗi lớp
   - một vài ảnh mẫu
4. Baseline không segmentation.
5. Segmentation pipeline:
   - K-means/HSV
   - morphology
   - crop vật thể
6. Contour và shape features:
   - contour lớn nhất
   - bounding box
   - area/perimeter/aspect ratio/circularity
7. Feature extraction:
   - HOG
   - shape features
8. Classifier:
   - SVM/k-NN
   - CNN head nếu làm mở rộng
9. Parameter sweep.
10. Quantitative evaluation:
   - accuracy
   - precision/recall/F1
   - confusion matrix
11. Qualitative evaluation:
   - ảnh dự đoán đúng
   - ảnh dự đoán sai
   - ảnh trung gian segmentation
12. Discussion:
   - giả thuyết đúng/sai/đúng một phần
   - lớp nào khó
   - hạn chế của segmentation
   - hướng cải thiện
13. Streamlit demo nếu có.
14. Conclusion.

## 12. Pipeline tóm tắt

```text
Input image
        |
        v
Resize + color normalization
        |
        v
Segmentation
K-means clustering / HSV threshold
        |
        v
Morphology cleaning
        |
        v
Find largest contour + crop object
        |
        v
Shape feature extraction
area, perimeter, aspect ratio, circularity
        |
        v
Feature extraction
HOG descriptor
        |
        v
Classifier
SVM
        |
        v
Predicted waste class
        |
        v
Metrics + confusion matrix + error analysis
```

## 13. Demo Streamlit

Ngoài notebook dùng để huấn luyện, khảo sát tham số và đánh giá định lượng, nhóm có thể xây dựng thêm một ứng dụng Streamlit để demo trực quan. Ứng dụng cho phép người dùng upload một ảnh rác chụp bằng điện thoại, sau đó hệ thống chạy pipeline đã huấn luyện để dự đoán loại rác.

Workflow demo:

```text
Upload ảnh từ điện thoại/máy tính
        |
        v
Hiển thị ảnh gốc
        |
        v
Tiền xử lý + segmentation + contour crop
        |
        v
Trích HOG + shape features
        |
        v
Load SVM model đã huấn luyện
        |
        v
Hiển thị nhãn dự đoán, độ tin cậy và ảnh trung gian
```

Giao diện Streamlit đề xuất:

- Upload ảnh `.jpg`, `.jpeg`, `.png`.
- Hiển thị ảnh gốc.
- Hiển thị mask phân đoạn hoặc ảnh crop vật thể.
- Hiển thị kết quả dự đoán:

```text
Dự đoán: plastic
Độ tin cậy: 87.3%
Nhóm xử lý: rác tái chế
```

- Hiển thị top-3 lớp dự đoán nếu classifier hỗ trợ xác suất.
- Gợi ý nhóm rác:

```text
plastic / paper / cardboard / glass / metal -> rác tái chế
organic -> rác hữu cơ
trash -> rác còn lại
```

Cấu trúc project đề xuất:

```text
lab/
  app.py
  lab.ipynb
  description.md
  models/
    garbage_classifier.pkl
    scaler.pkl
  data/
    garbage/
      train/
      val/
      test/
  output/
    figures/
    confusion_matrix.png
    predictions/
```

Vai trò của notebook và Streamlit:

```text
Notebook:
- Chuẩn bị dữ liệu.
- Huấn luyện model.
- Khảo sát tham số.
- Đánh giá accuracy, precision, recall, F1-score.
- Vẽ confusion matrix.
- Lưu model ra file.

Streamlit:
- Load model đã huấn luyện.
- Nhận ảnh upload từ người dùng.
- Chạy cùng pipeline tiền xử lý/phân đoạn/contour.
- Hiển thị kết quả dự đoán và ảnh trung gian.
```

Lưu ý: Streamlit chỉ là phần demo trực quan. Phần chấm điểm chính vẫn cần notebook/báo cáo có đầy đủ thí nghiệm, ảnh trung gian, parameter sweep và đánh giá định lượng theo yêu cầu lab_CK.

## 14. Vì sao đề tài này phù hợp lab_CK?

- Có vấn đề thực tế rõ ràng: phân loại rác hỗ trợ tái chế.
- Dùng dữ liệu ảnh thật, không phải dữ liệu tổng hợp.
- Có ít nhất 3 kỹ thuật trong chương trình:
  - Chương 2: tiền xử lý ảnh.
  - Chương 3: contour và shape features.
  - Chương 4: phân đoạn ảnh bằng K-means/HSV/morphology.
  - Chương 5: nhận dạng ảnh bằng HOG+SVM hoặc CNN transfer learning.
- Có ít nhất 2 kỹ thuật thuộc Chương 3/4/5:
  - Chương 3: contour/shape feature.
  - Chương 4: segmentation.
  - Chương 5: classification.
- Có đánh giá định lượng rõ ràng:
  - accuracy, precision, recall, F1-score, confusion matrix.
- Có ảnh trung gian và parameter sweep theo đúng yêu cầu lab_CK.

