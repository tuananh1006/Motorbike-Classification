from PIL import Image
import torchvision
import torchvision.transforms as transforms
import torch
from torch import nn
import torchvision.models as models
import os

os.environ["CUDA_LAUNCH_BLOCKING"] = "0"

def define_device():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return device

def load_model(model_path, device):
    model_ft = models.regnet_y_128gf(weights='RegNet_Y_128GF_Weights.IMAGENET1K_SWAG_LINEAR_V1')
    num_ftrs = model_ft.fc.in_features
    model_ft.fc = nn.Sequential(
        nn.Linear(num_ftrs, 1024),
        nn.ReLU(),
        nn.Dropout(0.5),
        nn.Linear(1024, 512),
        nn.ReLU(),
        nn.Dropout(0.5),
        nn.Linear(512, 5)  # Assuming you have 5 classes
    )
    model_ft.load_state_dict(torch.load('./model/model.pt',map_location=device))

    return model_ft

def transform_img():
    transform = transforms.Compose([
        transforms.Resize(384, interpolation=Image.BILINEAR),
        transforms.CenterCrop(384),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform

def predict(model, device, img_path, transform):
    img = None
    img = Image.open(img_path).convert('RGB')
    transform_using = transform()
    img = transform_using(img).unsqueeze(0)
    with torch.no_grad():
        outputs = model(img)
        _, preds = torch.max(outputs, 1)
    return preds.item()

if __name__ == "__main__":
    device = define_device()
    # device=torch.device("cpu")
    model = load_model("./model/model.pt", device)
    img_path = "./data/test.jpg"
    print(f"Result: {predict(model, device, img_path, transform_img)}")