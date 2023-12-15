import cv2

# Open webcam
cap = cv2.VideoCapture(0)


if __name__ == '__main__':
  while True:
    # Capture frame
    ret, frame = cap.read()

    # Show original, grayscale, and binary frames
    cv2.imshow('Original', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

# Release capture
cap.release()
cv2.destroyAllWindows()