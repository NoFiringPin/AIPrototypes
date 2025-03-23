import torch

# Download YOLOv5 from PyTorch Hub
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Supported classes
print("Supported classes")
print(model.names)
print()

# Sample Image URL
BASE_URL = 'https://github.com/ultralytics/yolov5/raw/master/data/images/'
FILE_NAMES = ['zidane.jpg', 'bus.jpg']

# A batch of images
imgs = [BASE_URL + file_name for file_name in FILE_NAMES]

# Inference
results = model(imgs)

# Display the results
results.show()

# Save the results
results.save()
print()

# Print the results
print("Results")
results.print()
print()

# Print the first bounding box values
print("Bounding box")
for i, file_name in enumerate(FILE_NAMES):
    print(file_name)
    print(results.xyxy[i])
    print()