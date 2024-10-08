from PIL import Image
import torchvision
import torchvision.transforms as transforms
import torch
from torch import nn
import torchvision.models as models
import os
import gdown

os.environ["CUDA_LAUNCH_BLOCKING"] = "0"

def define_device():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    return device

#down file from link drive
def download_model():
    #make path model if not exists
    if not os.path.exists('./model'):
        os.makedirs('./model')
    if not os.path.exists('./model/model.pt'):
        url = "https://drive.google.com/uc?id=1DY1tSYKOcFmpAKnjBIDyv3VF7OUebQ7W&export=download"
        output = "./model/model.pt"
        gdown.download(url, output, quiet=False)
        return True
    else:
        return False
def load_model( device):
    check = download_model()
    if check==True:
        print("Download model success")
    else:
        print("Model already exists")
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
    #List current directory
    model_ft.load_state_dict(torch.load('./model/model.pt',map_location=device))
    print("Load model success")
    return model_ft

def transform_img():
    transform = transforms.Compose([
        transforms.Resize(384, interpolation=Image.BILINEAR),
        transforms.CenterCrop(384),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform

def predict(model, device, img):
    transform_using = transform_img()
    img = transform_using(img).unsqueeze(0)
    with torch.no_grad():
        outputs = model(img)
        _, preds = torch.max(outputs, 1)
    return preds.item()

if __name__ == "__main__":
    device = define_device()
    # device=torch.device("cpu")
    model = load_model( device)
    img_path = "./data/test.jpg"
    img=Image.open(img_path).convert('RGB')
    print(f"Result: {predict(model, device, img)}")