import numpy as np
from skimage import color
import rawpy
import cv2
from aatcc_gray_score import aatcc_gray_score as gray
from iso_105_a05_ssr import calculate_iso_105_a05_ssr as iso
from aatcc_staining_score import aatcc_staining_score as stain


def raw_to_Lab(raw_path1, raw_path2):
    try:
        scale = input("Plese define what color grading scale you would like to compare these samples on. Type '1' for AATCC Grayscale for Color Change, '2' for ISO 105-A05 SSR for Color Change, or '3' for AATCC Gray Scale for Staining: ")
    except ValueError:
        print("Invalid input. Please enter a number (1, 2, or 3).")
        return None
    roi_lib = {}
    for img_path in [raw_path1, raw_path2]:
        img = cv2.imread(img_path)
    
        roi = cv2.selectROI("Select Region of Interest", img, showCrosshair=True) #open a window to select the ROI, SPACE or ENTER to confirm, 'c' to cancel
        cv2.destroyAllWindows()

        x, y, w, h = roi #returns the coordinates of the selected ROI as (x, y, width, height)
        y1, y2 = y, y + h
        x1, x2 = x, x + w

        roi_lib[img_path] = (y1, y2, x1, x2)
    
    with rawpy.imread(raw_path1) as raw1, rawpy.imread(raw_path2) as raw2:
        rgb_linear1 = raw1.postprocess(gamma=(1, 1), no_auto_bright=True, output_bps=16)
        rgb_linear2 = raw2.postprocess(gamma=(1, 1), no_auto_bright=True, output_bps=16)

        # Normalize the RGB values to [0, 1] range for skimage color conversion
        rgb_normalized1 = rgb_linear1 / 65535.0 
        rgb_normalized2 = rgb_linear2 / 65535.0

        #Clip the values to [1e-10, 1] range to avoid any potential issues with color conversion with zeros
        rgb_normalized1 = np.clip(rgb_normalized1, 1e-10, 1)
        rgb_normalized2 = np.clip(rgb_normalized2, 1e-10, 1)
        
        Lab_image1 = color.rgb2lab(rgb_normalized1)
        Lab_image2 = color.rgb2lab(rgb_normalized2)
        
        Lab_roi1 = np.mean(Lab_image1[roi_lib[raw_path1][1]:roi_lib[raw_path1][3], roi_lib[raw_path1][0]:roi_lib[raw_path1][2]], axis=(0, 1))
        Lab_roi2 = np.mean(Lab_image2[roi_lib[raw_path2][1]:roi_lib[raw_path2][3], roi_lib[raw_path2][0]:roi_lib[raw_path2][2]], axis=(0, 1))

    if scale == '1':
        print(gray(Lab_roi1, Lab_roi2))
    elif scale == '2':
        ssr_value = iso(Lab_roi1, Lab_roi2)
        print(f"ISO 105-A05 Rating (SSR): {ssr_value:.2f}")
    elif scale == '3':
        print(stain(Lab_roi1, Lab_roi2))
  
       
    return Lab_roi1, Lab_roi2
    
if __name__ == "__main__":
    raw_path1 = "BlueTS_Raw.dng"
    raw_path2 = "GrayTS_Raw.dng"
        
    delta_e_test = raw_to_Lab(raw_path1, raw_path2)
