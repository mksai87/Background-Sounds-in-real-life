import cv2
import urllib.request
import numpy as np
import threading

# Replace the URL with the IP camera's stream URL
url = 'http://192.168.130.97/cam-lo.jpg'
cv2.namedWindow("live Cam Testing", cv2.WINDOW_AUTOSIZE)

# Create a function to fetch images asynchronously   
def fetch_images():
    global imgnp
    while True:
        try:
            img_resp = urllib.request.urlopen(url)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        except Exception as e:
            print("Error fetching image:", e)

# Start the image fetching thread
fetch_thread = threading.Thread(target=fetch_images)
fetch_thread.daemon = True
fetch_thread.start()

# Read and display video frames
while True:
    if 'imgnp' not in globals():
        continue
    
    # Decode the image
    im = cv2.imdecode(imgnp, -1)

    # Display the image
    cv2.imshow('live Cam Testing', im)
    key = cv2.waitKey(5)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
