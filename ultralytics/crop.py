import cv2

def crop_area(image):
    cropped_area = image[1020:1660, 1020:1660]
    return cropped_area

file = ('C:/workspace/maketek/images/20240118/1664_145957.jpg')
image = cv2.imread(file)
# print(image.shape)

# cv2.imshow('image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

cropped = crop_area(image)
# cv2.imshow('cropped', cropped)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

cv2.imwrite('C:/workspace/maketek/images/20240118/1664_145957_crop2.jpg', cropped)

