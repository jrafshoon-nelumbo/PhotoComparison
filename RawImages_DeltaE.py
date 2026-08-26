import numpy as np
from skimage import color
import rawpy
import cv2


def raw_to_delta_e(raw_path1, raw_path2):
    
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

        #Clip the values to [0, 1] range to avoid any potential issues with color conversion
        rgb_normalized1 = np.clip(rgb_normalized1, 1e-10, 1)
        rgb_normalized2 = np.clip(rgb_normalized2, 1e-10, 1)
        
        Lab_image1 = color.rgb2lab(rgb_normalized1)
        Lab_image2 = color.rgb2lab(rgb_normalized2)
        
        Lab_roi1 = np.mean(Lab_image1[roi_lib[raw_path1][1]:roi_lib[raw_path1][3], roi_lib[raw_path1][0]:roi_lib[raw_path1][2]], axis=(0, 1))
        Lab_roi2 = np.mean(Lab_image2[roi_lib[raw_path2][1]:roi_lib[raw_path2][3], roi_lib[raw_path2][0]:roi_lib[raw_path2][2]], axis=(0, 1))
        
        delta_e = np.linalg.norm(Lab_roi1 - Lab_roi2)
        
    return delta_e, Lab_roi1, Lab_roi2

def aatcc_score_color(delta_e):
    if 0.0 <= delta_e < 0.2:
        return "Color change grade is 5"
    elif 0.2 <= delta_e < 1.0:
        return "Color change grade is  4-5"
    elif 1.0 <= delta_e < 2.0:
        return "Color change grade is 4"
    elif 2.0 <= delta_e < 2.7:
        return "Color change grade is 3-4"
    elif 2.7 <= delta_e < 3.8:
        return "Color change grade is 3"
    elif 3.8 <= delta_e < 5.3:
        return "Color change grade is 2-3"
    elif 5.3 <= delta_e < 7.4:
        return "Color change grade is 2"
    elif 7.4 <= delta_e < 10.3:
        return "Color change grade is 1-2"  
    elif 10.3 <= delta_e < 14.6:
        return "Color change grade is 1"
    else:
        return "Ahhhhhhh spooky too much color change! Grade is 0"

    
if __name__ == "__main__":
    raw_path1 = "BlueTS_Raw.dng"
    raw_path2 = "GrayTS_Raw.dng"
        
    delta_e_test = raw_to_delta_e(raw_path1, raw_path2)
    print(f"Delta E value is: {delta_e_test[0]:.1f}")  
    print(aatcc_score_color(delta_e_test[0])) 
    print(delta_e_test[0], delta_e_test[1], delta_e_test[2])    