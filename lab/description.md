# TOPIC

Xây dựng và đánh giá hiệu quả các thuật toán trong bài toán phân loại hình ảnh rác tái chế.

# Purpose/Goal

## Tóm tắt định hướng nghiên cứu

Đề tài này được định hướng như một bài toán thực nghiệm đánh giá pipeline, không chỉ là một ứng dụng dự đoán nhãn đơn lẻ. Trọng tâm của dự án là **thực nghiệm và đánh giá**: trong bài toán phân loại rác tái chế, nhóm kiểm tra xem các bước xử lý ảnh cổ điển như K-means segmentation, contour crop và shape features có cải thiện kết quả phân loại so với baseline hay không.

## Phát biểu mục tiêu / giả thuyết / tiêu chí thành công

**Vấn đề:** Nhóm giải quyết bài toán phân loại hình ảnh rác trên bộ dữ liệu TrashNet gồm 6 lớp: `cardboard`, `glass`, `metal`, `paper`, `plastic` và `trash`. Đây là bài toán có ý nghĩa thực tế trong các hệ thống hỗ trợ phân loại rác tái chế, thùng rác thông minh và dây chuyền xử lý rác bán tự động.

**Giả thuyết chính:** Pipeline có K-means segmentation, contour crop và shape features sẽ cho kết quả tốt hơn baseline HOG + SVM trực tiếp trên ảnh gốc, vì bước phân đoạn/crop có thể giảm ảnh hưởng của nền ảnh và shape features bổ sung thông tin hình dạng cho HOG.

**Giả thuyết mở rộng:** Bổ sung HSV color histogram vào HOG có thể cải thiện kết quả phân loại, vì màu sắc, độ sáng và độ bão hòa màu là thông tin quan trọng để phân biệt các loại rác như glass, plastic, metal và paper.

**Tiêu chí thành công:** Giả thuyết được kiểm chứng bằng `accuracy`, `macro-F1`, `weighted-F1`, classification report, confusion matrix và thời gian dự đoán trung bình mỗi ảnh. Pipeline proposed được xem là cải thiện nếu có `accuracy` hoặc `macro-F1` cao hơn baseline trên cùng tập test.

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

- K-means: số cụm `k = 2, 3, 4`.
- HSV color histogram: số bin màu `8`, `16`, `32`.
- Các tham số morphology kernel, contour min area và pixels per cell được giữ cố định trong pipeline chính.
- HOG: orientations `6`, `9`, `12`.
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

## Cơ sở tài liệu và phạm vi so sánh

Đồ án này chỉ thực nghiệm trên bộ dữ liệu TrashNet. Các tài liệu liên quan được sử dụng để tạo bối cảnh và cơ sở lựa chọn phương pháp, không dùng để so sánh tuyệt đối giữa các dataset khác nhau.

Nguồn chính:

- **TrashNet**: dataset rác 6 lớp gồm `glass`, `paper`, `cardboard`, `plastic`, `metal`, `trash`, tổng 2527 ảnh. Đây là dữ liệu thực nghiệm chính của đồ án. Link: https://github.com/garythung/trashnet
- **Recyclable Waste Identification Using CNN Image Recognition and Gaussian Clustering**: nghiên cứu sử dụng TrashNet/augmented TrashNet với CNN và clustering, dùng làm bối cảnh tham khảo cho hướng deep learning mạnh hơn. Link: https://arxiv.org/abs/2011.01353
- **HOG**: Dalal and Triggs, CVPR 2005, là cơ sở cho đặc trưng Histogram of Oriented Gradients.
- **SVM**: Cortes and Vapnik, Machine Learning 1995, là cơ sở cho bộ phân loại Support Vector Machine.

Cơ sở đánh giá chính trong đồ án là so sánh nội bộ giữa các pipeline trên cùng TrashNet, cùng cách chia train/test và cùng metric. Vì mỗi tài liệu có thể dùng cách chia dữ liệu, augmentation, mô hình và điều kiện huấn luyện khác nhau, kết quả trong tài liệu chỉ được dùng làm bối cảnh, không dùng để kết luận mô hình của nhóm tốt hơn hoặc kém hơn một cách tuyệt đối.

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
| Proposed 2 | Ảnh gốc -> K-means segmentation -> contour crop -> HOG + shape features -> SVM | Pipeline chính trong 4 pipeline theo đề tài |
| Extension | Ảnh gốc -> Resize -> HOG + HSV color histogram -> SVM | Pipeline mở rộng để kiểm tra vai trò của màu sắc |

Kết quả thực nghiệm hiện tại cho thấy trong 4 pipeline chính, `Proposed 2` là pipeline tốt nhất. Tuy nhiên, khi xét thêm pipeline mở rộng, `Optimized HOG + HSV + SVM` đạt kết quả cao nhất và phù hợp hơn để dùng làm mô hình demo thực tế.


Ghi chú sau parameter sweep: notebook đã train lại mô hình với tham số tốt nhất từ sweep, gồm `HOG orientations = 6`, `HSV bins = 32` và SVM RBF `C = 10`. Mô hình optimized đạt accuracy khoảng 68.77%, cao hơn HOG + HSV mặc định 67.79%, nên đây là mô hình được chọn để lưu và dùng cho demo.

Tóm tắt kết quả đã chạy:

| Pipeline | Accuracy | Macro-F1 | Nhận xét |
|---|---:|---:|---|
| Baseline 1: HOG + SVM | 58.70% | 0.5962 | Baseline cơ bản, chạy nhanh |
| Baseline 2: HOG + Shape + SVM | 58.50% | 0.5959 | Shape features chưa cải thiện khi chưa crop |
| Proposed 1: K-means crop + HOG + SVM | 60.28% | 0.5911 | Segmentation/crop giúp tăng accuracy nhẹ |
| Proposed 2: K-means crop + HOG + Shape + SVM | 60.87% | 0.5965 | Tốt nhất trong 4 pipeline chính |
| Tuned HOG + SVM | 65.42% | 0.6472 | Tuning kernel RBF cải thiện rõ |
| Extension: HOG + HSV + SVM | 67.79% | 0.6671 | Mô hình mở rộng trước tối ưu |
| Optimized HOG(6) + HSV(32) + SVM | 68.77% | 0.6755 | Tốt nhất toàn bộ thí nghiệm, nên dùng cho demo |

Các tham số chính đã được khảo sát trong notebook:

- K-means segmentation: số cụm `k = 2, 3, 4`.
- HOG: số hướng gradient `orientations = 6, 9, 12`.
- HSV color histogram: số bin màu `8, 16, 32`.
- SVM: `C = 0.1`, `1`, `10`; kernel `linear`, `rbf`.

Các tham số morphology kernel, contour min area và pixels per cell được cố định trong pipeline chính để giữ thời gian chạy hợp lý; có thể xem là hướng mở rộng nếu tiếp tục tối ưu.

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
  - Có thể mở rộng sang dataset ảnh rác ngoài môi trường nếu muốn nghiên cứu detection/segmentation trong tương lai.

Input của chương trình:

- Một ảnh RGB/BGR chứa vật thể rác.
- Tập train/validation/test đã chia theo nhãn lớp.
- Tham số pipeline: kích thước ảnh, phương pháp segmentation, kích thước kernel morphology, tham số HOG/SVM và số bin HSV.

# Output

Output trung gian:

- Ảnh resize.
- Ảnh grayscale hoặc ảnh màu đã chuẩn hóa.
- Mask phân đoạn vật thể rác.
- Mask sau morphology.
- Bounding box hoặc crop vùng vật thể chính.
- Vector đặc trưng HOG, shape features hoặc HSV color histogram.

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
Trích đặc trưng HOG, shape features hoặc HSV color histogram
    |
    v
Classifier
    |
    v
Nhãn rác
```

Các bước:

1. Đọc ảnh bằng OpenCV/PIL.
2. Resize ảnh về kích thước cố định, ví dụ 128x128 cho HOG/SVM.
3. Chuẩn hóa giá trị pixel.
4. Trích đặc trưng:
   - HOG cho baseline cổ điển.
   - Hoặc HSV color histogram nếu kiểm tra vai trò của màu sắc.
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

- Kích thước ảnh chính: `128x128`; có thể thử thêm kích thước khác nếu mở rộng.
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

### HSV Color Histogram

Pipeline:

1. Resize ảnh về kích thước cố định.
2. Chuyển ảnh từ RGB sang HSV.
3. Tính histogram riêng cho kênh H, S và V.
4. Chuẩn hóa histogram.
5. Ghép histogram HSV với vector HOG.
6. Đưa vector đặc trưng vào SVM.

Parameter sweep:

- Số bin cho từng kênh HSV: 8, 16, 32.
- Không gian màu: RGB, HSV, Lab.
- Có/không ghép HSV với HOG.

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

6. Mở rộng đặc trưng màu:
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

Ngoài 4 pipeline chính, nhóm thử thêm pipeline mở rộng `HOG + HSV + SVM` để kiểm tra vai trò của màu sắc. Kết quả cho thấy pipeline này đạt accuracy cao nhất, nên có thể dùng làm mô hình demo thực tế. Tuy nhiên, khi trình bày theo yêu cầu đề tài, nhóm vẫn cần báo cáo đủ 4 pipeline chính để chứng minh quá trình đánh giá baseline và proposed.

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
   - SVM
   - HSV color histogram nếu làm mở rộng
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

Lưu ý quan trọng: phần thí nghiệm chính vẫn báo cáo đủ 4 pipeline `Baseline 1`, `Baseline 2`, `Proposed 1` và `Proposed 2`. Riêng phần demo thực tế dùng mô hình có kết quả cao nhất trong thí nghiệm mở rộng, tức `Optimized HOG + HSV + SVM`, vì pipeline này đạt accuracy tốt nhất.

Workflow demo dùng mô hình tốt nhất:

```text
Upload ảnh từ điện thoại/máy tính
        |
        v
Hiển thị ảnh gốc
        |
        v
Resize ảnh về 128x128
        |
        v
Trích HOG feature + HSV color histogram
        |
        v
Load SVM RBF đã huấn luyện
        |
        v
Hiển thị nhãn dự đoán và điểm decision score
```

Giao diện Streamlit đề xuất:

- Upload ảnh `.jpg`, `.jpeg`, `.png`.
- Hiển thị ảnh gốc.
- Hiển thị ảnh sau resize và biểu đồ HSV histogram nếu muốn minh họa pipeline.
- Hiển thị kết quả dự đoán:

```text
Dự đoán: plastic
Mô hình: Optimized HOG + HSV + SVM
Nhóm xử lý: rác tái chế
```

- Hiển thị top-3 lớp theo decision score nếu classifier hỗ trợ.
- Gợi ý nhóm rác:

```text
plastic / paper / cardboard / glass / metal -> rác tái chế
trash -> rác còn lại
```

Cấu trúc project đề xuất:

```text
lab/
  app.py
  lab.ipynb
  description.md
  models/
    hog_hsv_svm.joblib
    model_metadata.joblib
  data/
    trashnet_resized/
  output/
    figures/
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
- Lưu model tốt nhất sau optimized sweep ra file.

Streamlit:
- Load model tốt nhất đã huấn luyện.
- Nhận ảnh upload từ người dùng.
- Chạy cùng pipeline tiền xử lý và trích đặc trưng HOG + HSV với tham số tốt nhất.
- Hiển thị kết quả dự đoán và các thông tin trung gian phù hợp.
```

Lưu ý: Streamlit chỉ là phần demo trực quan. Phần chấm điểm chính vẫn cần notebook/báo cáo có đầy đủ thí nghiệm, ảnh trung gian, parameter sweep và đánh giá định lượng theo yêu cầu lab_CK.

## 14. Vì sao đề tài này phù hợp lab_CK?

- Có vấn đề thực tế rõ ràng: phân loại rác hỗ trợ tái chế.
- Dùng dữ liệu ảnh thật, không phải dữ liệu tổng hợp.
- Có ít nhất 3 kỹ thuật trong chương trình:
  - Chương 2: tiền xử lý ảnh.
  - Chương 3: contour và shape features.
  - Chương 4: phân đoạn ảnh bằng K-means/HSV/morphology.
  - Chương 5: nhận dạng ảnh bằng HOG+SVM, tuning SVM và đặc trưng màu HSV.
- Có ít nhất 2 kỹ thuật thuộc Chương 3/4/5:
  - Chương 3: contour/shape feature.
  - Chương 4: segmentation.
  - Chương 5: classification.
- Có đánh giá định lượng rõ ràng:
  - accuracy, precision, recall, F1-score, confusion matrix.
- Có ảnh trung gian và parameter sweep theo đúng yêu cầu lab_CK.



## Tài liệu tham khảo chính

1. G. Thung, M. Yang, **TrashNet: Dataset of images of trash**, Stanford CS229 project repository. https://github.com/garythung/trashnet
2. Y. Wang, W. J. Zhao, J. Xu, R. Hong, **Recyclable Waste Identification Using CNN Image Recognition and Gaussian Clustering**, arXiv:2011.01353, 2020. https://arxiv.org/abs/2011.01353
3. N. Dalal, B. Triggs, **Histograms of Oriented Gradients for Human Detection**, CVPR 2005.
4. C. Cortes, V. Vapnik, **Support-Vector Networks**, Machine Learning, 1995.
