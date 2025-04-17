import torch
import os
from torchvision import transforms
import cv2
import numpy as np
import matplotlib.pyplot as plt
from csrnet.model import CSRNet

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

# Loading Images for Crowd Counting
img_path = "crowdtest.jpg"
img = cv2.imread(img_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_tensor = transform(img).unsqueeze(0)

with torch.no_grad():
    model_output = model(img_tensor)
    count = torch.sum(model_output).item()

print(f"Crowd Count Estimate: {int(count)}")
