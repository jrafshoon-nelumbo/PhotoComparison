import cv2

# Load a preview image (or converted raw)
img = cv2.imread("BlueTS_Raw.dng")  # Replace with your image path

# Open a window where you can click and drag a rectangle over the fabric
# Press SPACE or ENTER after selecting, or 'c' to cancel
bbox = cv2.selectROI("Select Fabric Region", img, showCrosshair=True)
cv2.destroyAllWindows()

# bbox returns (x, y, width, height)
x, y, w, h = bbox

# Convert to (y1, y2, x1, x2) for array slicing
y1, y2 = y, y + h
x1, x2 = x, x + w

print(f"Your ROI coordinates are: y1={y1}, y2={y2}, x1={x1}, x2={x2}")
