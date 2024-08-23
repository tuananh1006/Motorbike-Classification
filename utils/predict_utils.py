#Importing the required libraries
from PIL import Image
import torchvision.transforms as transforms
import torch
# Function to preprocess the image
def preprocess_image(image_path):
    """Load and preprocess an image."""
    # Define the transforms
    transform = transforms.Compose([
        transforms.Resize(384, interpolation=Image.BILINEAR),
        transforms.CenterCrop(384),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Load the image
    image = Image.open(image_path).convert('RGB')

    # Apply the transforms
    image = transform(image)

    # Add batch dimension
    image = image.unsqueeze(0)

    return image

def predict_single_image(image_path, model, device):
    """Predict the class of a single image using the trained model."""
    # Preprocess the image
    image = preprocess_image(image_path)

    # Move the image to the device
    image = image.to(device)

    # Set the model to evaluation mode
    model.eval()

    # Disable gradient computation
    with torch.no_grad():
        # Forward pass
        outputs = model(image)
        _, preds = torch.max(outputs, 1)

    return preds.item()

if __name__ == '__main__':
    image_path = 'data/test.jpg'
    # Predict the class of the image
    predicted_class = predict_single_image(image_path, model_ft, device)

    # Print the predicted class
    print(f'The predicted class for the image is: {predicted_class}')