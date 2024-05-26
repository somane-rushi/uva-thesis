import ultralytics
from ultralytics import YOLO
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
from IPython.display import display, Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from PIL import Image as PILImage

# Check environment
ultralytics.checks()

# Load YOLO model
model = YOLO('yolov8n.pt')

# Set image source
main_img = 'original/SK-C-535.jpg'
main_img_name = os.path.splitext(os.path.basename(main_img))[0]
# Change this as per the detected class
class_id = 43

results = model.predict(source=main_img, conf=0.15, classes=[class_id])

# Known classes
class_names = {
    0: 'person',  8: 'boat', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 26: 'handbag', 28: 'suitcase', 39: 'bottle',        
    40: 'wine glass',
    41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana',
    47: 'apple', 48: 'sandwich', 49: 'orange', 54: 'donut', 55: 'cake', 56: 'chair', 58: 'potted plant', 60: 'dining table',
    73: 'book', 75: 'vase'
}

# Extract bounding box coordinates
for result in results:
    boxes = result.boxes

bbox = boxes.xyxy.tolist()[0]

class_name = class_names[class_id]

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

# Create a folder for outputs named after the input file name inside 'runs'
output_base_dir = 'runs'
if not os.path.exists(output_base_dir):
    os.makedirs(output_base_dir)

output_dir_base = os.path.join(output_base_dir, f"{main_img_name}_output")
output_dir = output_dir_base
counter = 1
while os.path.exists(output_dir):
    output_dir = f"{output_dir_base}_{counter}"
    counter += 1
os.makedirs(output_dir)

# Plot and save the image with the mask
fig, ax = plt.subplots(figsize=(15, 15))  # Set figure size to 1500 pixels width
ax.imshow(image)
show_mask(masks[0], ax)
show_box(input_box, ax)
ax.axis('off')

# Save the image with mask
output_image_path = os.path.join(output_dir, f'Mask_{main_img_name}_{class_name}.jpg')
plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0, dpi=100)

# Create and save segmented image with transparent background
segmentation_mask = masks[0]
binary_mask = np.where(segmentation_mask > 0.5, 1, 0).astype(np.uint8)

# Create a transparent background
transparent_background = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)

# Apply the mask to create the segmented image with transparency
new_image = transparent_background.copy()
new_image[..., :3] = image * binary_mask[..., np.newaxis]
new_image[..., 3] = binary_mask * 255

# Convert to PIL Image and save
segmented_image_path = os.path.join(output_dir, f'Segment_{main_img_name}_{class_name}.png')
segmented_image_pil = PILImage.fromarray(new_image)
segmented_image_pil.save(segmented_image_path)

# Resize output_image_with_mask to 1500px width if it's not already
with PILImage.open(output_image_path) as img:
    img_width, img_height = img.size
    if img_width != 1500:
        new_height = int((1500 / img_width) * img_height)
        resized_img = img.resize((1500, new_height), PILImage.Resampling.LANCZOS)
        resized_img.save(output_image_path)

# Calculate bounding box coordinates in percentages relative to the original image dimensions
img_height, img_width = image.shape[:2]
percent_bbox = {
    "width": round((bbox[2] - bbox[0]) / img_width * 100, 1),
    "height": round((bbox[3] - bbox[1]) / img_height * 100, 1),
    "top": round(bbox[1] / img_height * 100, 1),
    "left": round(bbox[0] / img_width * 100, 1)
}

# Save the bounding box details in percentages to a separate JSON file
percent_bbox_path = os.path.join(output_dir, 'percent_bbox_coordinates.json')
with open(percent_bbox_path, 'w') as f:
    json.dump(percent_bbox, f)

# Display the final output image
# plt.show()
