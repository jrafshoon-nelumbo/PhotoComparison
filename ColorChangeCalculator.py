import numpy as np
from skimage import color
import rawpy

# 1. Load RAW file linearly
with rawpy.imread("sample_raw_image.dng") as raw:
    # Extract linear RGB image (no gamma correction)
    rgb_linear = raw.postprocess(
        gamma=(1, 1), no_auto_bright=True, output_bps=16
    )

# 2. Convert Linear RGB to CIELAB
# Note: Ensure custom color profile calibration matrix is applied for best accuracy
rgb_normalized = rgb_linear / 65535.0
lab_image = color.rgb2lab(rgb_normalized)

# 3. Sample Regions of Interest (ROIs) [y1:y2, x1:x2]
lab_original = np.mean(lab_image[100:200, 100:200], axis=(0, 1))
lab_tested = np.mean(lab_image[100:200, 300:400], axis=(0, 1))

# 4. Compute Delta E (CIELAB)
delta_e = np.linalg.norm(lab_original - lab_tested)
print(f"Calculated Delta E: {delta_e:.2f}")
