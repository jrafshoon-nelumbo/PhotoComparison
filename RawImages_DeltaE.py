import numpy as np
from skimage import color
import rawpy


def raw_to_delta_e(raw_path1, raw_path2, roi1, roi2):
    """
    Calculate Delta E between two RAW images in specified ROIs.
    
    Parameters:
        raw_path1 (str): Path to the first RAW image.
        raw_path2 (str): Path to the second RAW image.
        roi1 (tuple): Region of interest for the first image (x1, y1, x2, y2).
        roi2 (tuple): Region of interest for the second image (x1, y1, x2, y2).
    
    Returns:
        float: Calculated Delta E value.
    """
    with rawpy.imread(raw_path1) as raw1, rawpy.imread(raw_path2) as raw2:
        rgb_linear1 = raw1.postprocess(gamma=(1, 1), no_auto_bright=True, output_bps=16)
        rgb_linear2 = raw2.postprocess(gamma=(1, 1), no_auto_bright=True, output_bps=16)
        
        rgb_normalized1 = rgb_linear1 / 65535.0
        rgb_normalized2 = rgb_linear2 / 65535.0
        
        lab_image1 = color.rgb2lab(rgb_normalized1)
        lab_image2 = color.rgb2lab(rgb_normalized2)
        
        lab_roi1 = np.mean(lab_image1[roi1[1]:roi1[3], roi1[0]:roi1[2]], axis=(0, 1))
        lab_roi2 = np.mean(lab_image2[roi2[1]:roi2[3], roi2[0]:roi2[2]], axis=(0, 1))
        
        delta_e = np.linalg.norm(lab_roi1 - lab_roi2)
        
    return delta_e


if __name__ == "__main__":
    # Example usage
    raw_path1 = "BlueTS_Raw.dng"
    raw_path2 = "GrayTS_Raw.dng"
    roi1 = (100, 200, 100, 200)  # ROI for the first image
    roi2 = (100, 200, 100, 200)  # ROI for the second image
    
    delta_e_value = raw_to_delta_e(raw_path1, raw_path2, roi1, roi2)
    print(f"Calculated Delta E: {delta_e_value:.2f}")