import numpy as np


def aatcc_gray_score(Lab_roi1, Lab_roi2):
    delta_e = delta_e = np.linalg.norm(Lab_roi1 - Lab_roi2)
    #This scale is a modified version of the AATCC Gray Scale for Color Change, which is based on the CIE 1976 color difference formula. It is done to remove the gaps in the scoring that are used when visually comparing color change.
    # The original AATCC Gray Scale for Color Change has the following ranges:
    # 0.0 - 0.2: Grade 5
    # 0.6 - 1.0: Grade 4-5
    # 1.4 - 2.0: Grade 4
    # 2.2 - 2.8: Grade 3-4
    # 3.0 - 3.8: Grade 3
    # 4.3 - 5.3: Grade 2-3
    # 6.2 - 7.4: Grade 2
    # 8.9 - 10.3: Grade 1-2
    # 12.6 - 14.6: Grade 1
    
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
        return "Color change grade is 1-2"
    elif 10.3 <= delta_e < 14.6:
        return "Color change grade is 1"
    else:
        return "Ahhhhhhh spooky too much color change! Grade is 0"
    