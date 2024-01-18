import glob
import cv2
import matplotlib.pyplot as plt
import os

files = glob.glob("*.jpg")

def show_diff(a,b):
    diff_image = cv2.absdiff(a, b)
    thresh = cv2.threshold(diff_image, 30, 255, cv2.THRESH_BINARY)[1]  # Adjust threshold as needed
    blended = cv2.addWeighted(a, 0.4, thresh, 0.6, 0)  # Adjust weights for desired blending
    plt.axis('off')
    plt.imshow(blended, cmap='magma')
    plt.savefig('diff_img.jpg')



a = cv2.imread(files[0], 0)
b = cv2.imread(files[1], 0)

show_diff(a,b)
