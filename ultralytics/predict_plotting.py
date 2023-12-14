from PIL import Image
from ultralytics import YOLO

# Load a pretrained YOLOv8n model
# model = YOLO('C:\\workspace\\maketek\\runs\\detect\\train3\\weights\\best.pt')  # pretrained YOLOv8n model
model = YOLO('C:\\workspace\\maketek\\runs\\segment\\train\\weights\\best.pt')  # pretrained YOLOv8n model

# Run inference on 'bus.jpg'
image = 'C:\\workspace\\maketek\\raw_151651.jpg'
images = ['C:\\workspace\\maketek\\raw_deform_spot_153353.jpg', \
            'C:\\workspace\\maketek\\raw_deform_spot_153430.jpg', \
            'C:\\workspace\\maketek\\raw_deform_spot_153603.jpg']

# results = model(image)  # results list
# Run inference on 'bus.jpg' with arguments
results = model.predict(images, save=False, imgsz=1080, conf=0.8)

# Show the results
if __name__ == '__main__':
    for r in results:
        im_array = r.plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
        # im.show()  # show image
        # im.save(images[r.names[0]]+'_results.jpg')  # save image
        im.save(r.path+'_results.jpg')  # save image