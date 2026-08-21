import numpy as np
from skimage import color
import rawpy
import cv2


def raw_to_delta_e(raw_path1, raw_path2):
    
    roi_lib = {}
    for img_path in [raw_path1, raw_path2]:
        img = cv2.imread(img_path)
    
        box = cv2.selectROI("Select Fabric Region", img, showCrosshair=True) #open a window to select the ROI, SPACE or ENTER to confirm, 'c' to cancel
        cv2.destroyAllWindows()

        x, y, w, h = box #returns the coordinates of the selected ROI as (x, y, width, height)
        y1, y2 = y, y + h
        x1, x2 = x, x + w

        roi_lib[img_path] = (y1, y2, x1, x2)
    
    with rawpy.imread(raw_path1) as raw1, rawpy.imread(raw_path2) as raw2:
        rgb_linear1 = raw1.postprocess(gamma=(1, 1), no_auto_bright=True, output_bps=16)
        rgb_linear2 = raw2.postprocess(gamma=(1, 1), no_auto_bright=True, output_bps=16)
        
        rgb_normalized1 = rgb_linear1 / 65535.0
        rgb_normalized2 = rgb_linear2 / 65535.0
        
        lab_image1 = color.rgb2lab(rgb_normalized1)
        lab_image2 = color.rgb2lab(rgb_normalized2)
        
        lab_roi1 = np.mean(lab_image1[roi_lib[raw_path1][1]:roi_lib[raw_path1][3], roi_lib[raw_path1][0]:roi_lib[raw_path1][2]], axis=(0, 1))
        lab_roi2 = np.mean(lab_image2[roi_lib[raw_path2][1]:roi_lib[raw_path2][3], roi_lib[raw_path2][0]:roi_lib[raw_path2][2]], axis=(0, 1))
        
        delta_e = np.linalg.norm(lab_roi1 - lab_roi2)
        
    return delta_e
#### Add in AATCC scoring for color change

if __name__ == "__main__":
    raw_path1 = "BlueTS_Raw.dng"
    raw_path2 = "GrayTS_Raw.dng"
        
    delta_e_value = raw_to_delta_e(raw_path1, raw_path2)
    print(f"Calculated Delta E: {delta_e_value:.3f}") #print the Delta E value with 3 decimal places for better precision 