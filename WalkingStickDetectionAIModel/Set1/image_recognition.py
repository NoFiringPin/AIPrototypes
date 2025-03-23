import torch
import cv2
import glob
import ultralytics

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# print to see which classes the model is able to detect
print("Supported Classes")
print(model.names)
print()

# Do not change the directory
image_directory = "/home/pi/"



# grab every image that ends in .jpg
image_paths = glob.glob(image_directory + "*.jpg")

# for loop that goes through every .jpg image in the directory
for path in image_paths:
    # read every image
    img = cv2.imread(path)
    
    
    
    # pass the images
    results = model(img)
    
    # print results
    results.print()
    
    # Render the results in a box
    image_with_boxes = results.render()[0]
    
    # Display the images
    cv2.imshow("Recognized Objects", image_with_boxes)
    cv2.waitKey(0)
    
    
cv2.destroyAllWindows()
    
    
