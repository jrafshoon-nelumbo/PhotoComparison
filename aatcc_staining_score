import numpy as np

def aatcc_staining_score(Lab_roi1, Lab_roi2):
    delta_e = np.linalg.norm(Lab_roi1 - Lab_roi2)
    
    if 0.0 <= delta_e <= 0.2:
        return "Staining grade is 5"
    elif 1.9 <= delta_e <= 2.5:
        return "Staining grade is 4-5"
    elif 4.0 <= delta_e <= 4.6:
        return "Staining grade is 4"
    elif 5.6 <= delta_e <= 6.4:
        return "Staining grade is 3-4"
    elif 8.0 <= delta_e <= 9.0:
        return "Staining grade is 3"
    elif 11.3 <= delta_e <= 12.7:
        return "Staining grade is 2-3"
    elif 15.9 <= delta_e <= 17.9:
        return "Staining grade is 2"
    elif 22.5 <= delta_e <= 25.5:
        return "Staining grade is 1-2"  
    elif 32.1 <= delta_e <= 36.1:
        return "Staining grade is 1"
    elif delta_e > 36.1:
        return "Ahhhhhhh spooky too much staining! Grade is 0"