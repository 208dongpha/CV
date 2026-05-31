import numpy as np
import json
import matplotlib.pyplot as plt
from scipy.ndimage import maximum_filter

# Đọc notebook
with open(r'd:\Dongphh\CVision\assignment_starter-2.ipynb', encoding='utf-8') as f:
    notebook = json.load(f)

# Lấy code từ cell 41 (CIRCLE_16 và các hàm FAST)
code1 = ''.join(notebook['cells'][41]['source'])

# Lấy code từ cell 42 (test code)
code2 = ''.join(notebook['cells'][42]['source'])

print("=" * 60)
print("CELL 41 - FAST Functions:")
print("=" * 60)
print(code1)
print()

# Thử chạy code
exec(code1)

# Tạo hàm make_test_image
def make_test_image(kind='rect', N=128):
    """Tạo ảnh tổng hợp để thử nghiệm."""
    img = np.zeros((N, N), dtype=np.float64)
    if kind == 'rect':
        img[N//4:3*N//4, N//4:3*N//4] = 1.0
    return img

# Test FAST detector
print("=" * 60)
print("Testing FAST Detector:")
print("=" * 60)

img_test = make_test_image('rect', N=128)
print(f"Test image shape: {img_test.shape}")
print(f"Image min/max: {img_test.min()}/{img_test.max()}")
print(f"Rectangle bounds: row 32:96, col 32:96")

# Thử với multiple threshold values
for t_val in [0.05, 0.10, 0.20, 0.35]:
    try:
        kps, smap = fast_detector(img_test, t=t_val, n=12, nms=True)
        print(f't={t_val:.2f}: {len(kps)} keypoints, score_map min/max: {smap.min()}/{smap.max()}')
        print(f'  Non-zero scores: {np.sum(smap > 0)}')
    except Exception as e:
        print(f't={t_val:.2f}: ERROR - {e}')

print()
print("Checking algorithm step-by-step at point (50, 50):")
print("=" * 60)

# Test at a single point that should be a corner (edge of rect)
test_r, test_c = 32, 50  # Top edge of rectangle
print(f"Testing pixel at ({test_r}, {test_c})")
print(f"Pixel value: {img_test[test_r, test_c]}")

for t_val in [0.1, 0.2]:
    try:
        is_c, score = fast_is_corner(img_test, test_r, test_c, t=t_val, n=12)
        print(f'  t={t_val}: is_corner={is_c}, score={score}')
    except Exception as e:
        print(f'  t={t_val}: ERROR - {e}')

# Try a point definitely in the middle
test_r2, test_c2 = 64, 64
print(f"\nTesting pixel at ({test_r2}, {test_c2})")
print(f"Pixel value: {img_test[test_r2, test_c2]}")
for t_val in [0.1, 0.2]:
    try:
        is_c, score = fast_is_corner(img_test, test_r2, test_c2, t=t_val, n=12)
        print(f'  t={t_val}: is_corner={is_c}, score={score}')
    except Exception as e:
        print(f'  t={t_val}: ERROR - {e}')

# Define nms_2d locally since it's missing
def nms_2d(response, window=9, threshold=0.0):
    """Non-Maximum Suppression 2D."""
    local_max = maximum_filter(response, size=window)
    return (response == local_max) & (response > threshold)

# Now test with nms_2d available
print("\n" + "=" * 60)
print("Testing with NMS (after defining nms_2d):")
print("=" * 60)

img_test = make_test_image('rect', N=128)
for t_val in [0.05, 0.10, 0.20]:
    kps, smap = fast_detector(img_test, t=t_val, n=12, nms=True)
    print(f't={t_val:.2f}: {len(kps)} keypoints')
    print(f'  Non-zero scores in map: {np.sum(smap > 0)}')

# Try with lower n parameter
print("\n" + "=" * 60)
print("Testing with lower n values:")
print("=" * 60)
for n_val in [9, 10, 11, 12]:
    kps, smap = fast_detector(img_test, t=0.1, n=n_val, nms=True)
    print(f'n={n_val}: {len(kps)} keypoints, non-zero scores: {np.sum(smap > 0)}')
