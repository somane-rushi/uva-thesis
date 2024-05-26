import ultralytics
from ultralytics import YOLO
import os
import json

# Check environment
ultralytics.checks()

# Load YOLO model
model = YOLO('yolov8n.pt')

# Set image source directory
image_dir = 'original/'

# Create output directory for JSON files
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# Known classes
class_names = {
    0: 'person', 14: 'bird', 15: 'cat', 16: 'dog', 39: 'bottle', 40: 'wine glass',
    41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana',
    47: 'apple', 48: 'sandwich', 49: 'orange', 54: 'donut', 55: 'cake', 56: 'chair',
    73: 'book', 75: 'vase'
}

# Process each image in the directory
for filename in os.listdir(image_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(image_dir, filename)
        results = model.predict(source=image_path, conf=0.15, classes=[40])

        # Collect top 3 objects based on confidence scores
        top_results = []
        for result in results:
            for i, box in enumerate(result.boxes.xyxy.tolist()):
                confidence = result.boxes.conf[i]
                class_id = result.boxes.cls[i]
                class_name = class_names[int(class_id)]
                top_results.append({'confidence': confidence, 'class': class_name})

        # Sort results by confidence and take top 3
        top_results = sorted(top_results, key=lambda x: x['confidence'], reverse=True)[:3]

        # Save results to JSON file
        json_path = os.path.join(output_dir, f'{os.path.splitext(filename)[0]}_results.json')
        with open(json_path, 'w') as json_file:
            json.dump(top_results, json_file, indent=4)

        print(f'Processed {filename}: {top_results}')
