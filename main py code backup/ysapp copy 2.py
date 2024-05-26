import ultralytics
from ultralytics import YOLO
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
from IPython.display import display, Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import json

# Check environment
ultralytics.checks()

# Load YOLO model
model = YOLO('yolov8n.pt')

# Set image source
main_img = 'original/SK-A-3.jpg'
results = model.predict(source=main_img, conf=0.15, classes=[0])
# Known classes
# { 0: 'person', 14: 'bird', 15: 'cat', 16: 'dog', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange',54: 'donut', 55: 'cake', 56: 'chair', 73: 'book', 75: 'vase',}

# Extract bounding box coordinates
for result in results:
    boxes = result.boxes

bbox = boxes.xyxy.tolist()[0]

# Load SAM model
sam_checkpoint = "sam_vit_h_4b8939.pth"
model_type = "vit_h"
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
predictor = SamPredictor(sam)

# Read and set image for SAM
image = cv2.cvtColor(cv2.imread(main_img), cv2.COLOR_BGR2RGB)
predictor.set_image(image)

# Functions for visualization
def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)

def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)

def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))

# Generate mask
input_box = np.array(bbox)
masks, _, _ = predictor.predict(
    point_coords=None,
    point_labels=None,
    box=input_box[None, :],
    multimask_output=False,
)

# Plot and save the image with the mask
plt.figure(figsize=(10, 10))
plt.imshow(image)
show_mask(masks[0], plt.gca())
show_box(input_box, plt.gca())
plt.axis('off')

# Create output directory if it doesn't exist
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the image with mask
output_image_path = os.path.join(output_dir, 'output_image_with_mask.png')
plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0)

# Save bounding box coordinates
bbox_path = os.path.join(output_dir, 'bbox_coordinates.json')
with open(bbox_path, 'w') as f:
    json.dump(bbox, f)  # No need for .tolist()

# Save mask coordinates
mask_coords = np.column_stack(np.where(masks[0] == True)).tolist()
mask_coords_path = os.path.join(output_dir, 'mask_coordinates.json')
with open(mask_coords_path, 'w') as f:
    json.dump(mask_coords, f)

# Display the final output image
plt.show()
