import cv2
from pyzbar.pyzbar import decode

# Open the default camera
cap = cv2.VideoCapture(0)

while True:
    # Read the frame from the camera
    ret, frame = cap.read()
    
    # Decode QR code in the frame
    decoded_objs = decode(frame)
    for obj in decoded_objs:
        # Draw a rectangle around the QR code
        #cv2.rectangle(frame, obj.rect.left, obj.rect.top, obj.rect.right, obj.rect.bottom, (0, 255, 0, 3))
        
        # Print the QR code text
        print("Entry granted: ", obj.data)
    
    # Show the frame
    cv2.imshow("Ticket Scanner ", frame)
    
    # Wait for key press
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()