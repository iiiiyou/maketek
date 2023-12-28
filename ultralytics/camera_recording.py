import cv2

# Create a VideoCapture object to capture the video from your camera
cap = cv2.VideoCapture(0)

# Create a VideoWriter object to write the recorded video to a file
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_02.mp4', fourcc, 80.0, (1080, 1080))

# Start a loop to capture and record the video frames
while True:
    ret, frame = cap.read()
    if ret:
        out.write(frame)
        cv2.imshow('frame', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release the VideoCapture and VideoWriter objects
cap.release()
out.release()

# Destroy all windows
cv2.destroyAllWindows()