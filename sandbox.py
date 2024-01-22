import numpy as np
import matplotlib.pyplot as plt 
import cv2 

a = 'C:/Users/admin/Downloads/1.png'
b = 'C:/Users/admin/Downloads/2.png'
c = 'C:/Users/admin/Downloads/3.png'

img_1 = cv2.imread(a,0)
img_2 = cv2.imread(b,0)
img_3 = cv2.imread(c,0)

plt.imshow(img_1, cmap='gray')
plt.imshow(img_2, cmap='gray')
plt.imshow(img_3, cmap='gray')

plt.hist(img_1)
plt.hist(img_2)
plt.hist(img_3)


crop_1 = img_1[35:45, 35:45]
crop_2 = img_2[10:20, 5:15]

plt.imshow(crop_1, cmap='gray')
plt.imshow(crop_2, cmap='gray')

plt.hist(img_1)
plt.hist(img_2)
