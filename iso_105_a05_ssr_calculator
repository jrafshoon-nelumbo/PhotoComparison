import numpy as np
import math

def calculate_iso_105_a05_ssr(Lab_roi1, Lab_roi2):
    
    L_1, a_1, b_1 = Lab_roi1
    L_2, a_2, b_2 = Lab_roi2   
    
    #Calculate Chroma (C) and Hue angle (h) in degrees
    C_1 = math.sqrt(a_1**2 + b_1**2)
    C_2 = math.sqrt(a_2**2 + b_2**2)
    
    h_1 = math.degrees(math.atan2(b_1, a_1)) % 360
    h_2 = math.degrees(math.atan2(b_2, a_2)) % 360
    
    #Standard CIELAB differences
    dL = L_2 - L_1          
    dC = C_2 - C_1
    da = a_2 - a_1
    db = b_2 - b_1
    
    #Calculate standard delta H
    #(Using the standard dH = sqrt(dE^2 - dL^2 - dC^2) ensuring no domain math errors)
    dE_ab_sq = dL**2 + da**2 + db**2
    dH_sq = dE_ab_sq - dL**2 - dC**2
    dH = math.sqrt(max(0, dH_sq)) # max(0) prevents precision issue negative roots
    #Assign sign to dH
    if (a_1 * b_2 - a_2 * b_1) < 0:
        dH = -dH
        
    # 3. Mean Chroma and Mean Hue Angle
    C_M = (C_1 + C_2) / 2.0
    
    # Handle mean hue wrap-around at 360 degrees
    if abs(h_2 - h_1) <= 180:
        h_M = (h_2 + h_1) / 2.0
    else:
        if (h_2 + h_1) < 360:
            h_M = (h_2 + h_1) / 2.0 + 180
        else:
            h_M = (h_2 + h_1) / 2.0 - 180
            
    # 4. Calculate damping factor D
    h_diff = abs(h_M - 280)
    if h_diff <= 180:
        x = (h_diff / 30.0)**2
    else:
        x = ((360 - h_diff) / 30.0)**2
        
    D = (dC * C_M * math.exp(-x)) / 100.0
    
    # 5. Calculate modified Chroma (dC_K) and Hue (dH_K)
    dC_K = dC - D
    dH_K = dH - D
    
    # 6. Calculate finalized CF and HF components
    dC_F = dC_K / (1.0 + (20.0 * C_M / 1000.0)**2)
    dH_F = dH_K / (1.0 + (10.0 * C_M / 1000.0)**2)
    
    # 7. Calculate modified color difference (dE_F)
    dE_F = math.sqrt(dL**2 + dC_F**2 + dH_F**2)
    
    # 8. Convert to Standard Specimen Rating (SSR)
    if dE_F <= 3.4:
        ssr = 5.0 - (dE_F / 1.7)
    else:
        ssr = 5.0 - (math.log10(dE_F / 0.85) / math.log10(2.0))
        
    # Standard dictates ratings are capped between 1 and 5
    return max(1.0, min(5.0, ssr))


if __name__ == "__main__":
#test Lab values
    mean_lab_A = [33.49205637, 18.21758719, 18.75735102]  # Reference fabric Lab values
    mean_lab_B = [34.12387882, 18.98491883, 19.08586749]  # Specimen fabric Lab values
    
    grade = calculate_iso_105_a05_ssr(mean_lab_A, mean_lab_B)
    print(f"ISO 105-A05 Rating (SSR): {grade:.2f}")