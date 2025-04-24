import torch
import os
from torchvision import transforms
import cv2
from .csrnet.model import CSRNet
import json

model = CSRNet()
script_dir = os.path.dirname(os.path.abspath(__file__))
weights_path = os.path.join(script_dir, "weights.pth")
checkpoint = torch.load(weights_path, map_location=torch.device("cpu"))
model.load_state_dict(checkpoint)
model.eval()

# Preprocessing the image to run more accurately on CSRNet
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229,0.224,0.225])
])

def count_people_in_image(path): # Loading image and estimating number of people in it
    img = cv2.imread(path)
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_to_count = transform(img).unsqueeze(0)
    except:
        if img is None: # Returns an error if image not found in file destination
            raise FileNotFoundError(f"No image found at: {path}")
        else:
            print("Unknown error")
    with torch.no_grad():
        model_output = model(img_to_count)
        count = torch.sum(model_output).item()
        return count
    
def pass_to_main(number):
    return number

def count_all_images():
    count_list = []
    images_dir = os.path.join(script_dir, "..", "images") # Images folder destination
    for filename in os.listdir(images_dir):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(images_dir, filename)
            try:
                count_list.append(count_people_in_image(img_path))
            except FileNotFoundError as error:
                print(error)
    return count_list

def run_image_count(img_name):
    img_path = os.path.join(script_dir, "..", "images", img_name) # Creates an absolute path for the image that doesn't depend on this file's location
    return count_people_in_image(img_path)

run_image_count("airportimage2.jpg")