import cv2
import numpy as np
from skimage import color

def calculate_grayscale_delta_e(img_path1, img_path2):
    # 1. Load images (BGR format)
    img1 = cv2.imread(img_path1)
    img2 = cv2.imread(img_path2)
    
    # 2. Convert BGR to RGB
    rgb1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    rgb2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    
    # 3. Convert to CIE L*a*b* color space
    lab1 = color.rgb2lab(rgb1)
    lab2 = color.rgb2lab(rgb2)
    
    # 4. Extract L* channel (Lightness)
    L1 = lab1[:, :, 0]
    L2 = lab2[:, :, 0]
    
    # 5. Compute mean pixel-wise Lightness Difference (Grayscale ΔE)
    delta_E_map = np.abs(L1 - L2)
    mean_delta_E = np.mean(delta_E_map)
    
    return mean_delta_E, delta_E_map

# Example usage:
# mean_de, de_map = calculate_grayscale_delta_e('sample_A.tif', 'sample_B.tif')
# print(f"Average Grayscale Delta E: {mean_de:.2f}")