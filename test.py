import cv2
import numpy as np

# Function to check lighting conditions in an image
def check_lighting(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Compute histogram of image
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    
    # Calculate average intensity (mean value of histogram)
    mean_intensity = np.mean(hist)
    
    # Define a threshold for normal lighting conditions
    if mean_intensity < 50 or mean_intensity > 100:
        return "Potential Spoofing (Lighting issue)"
    else:
        return "Normal Lighting"

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    # Check lighting conditions in the frame
    lighting_status = check_lighting(frame)
    print(lighting_status)

    # Display the video frame
    cv2.imshow('Video Feed', frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()