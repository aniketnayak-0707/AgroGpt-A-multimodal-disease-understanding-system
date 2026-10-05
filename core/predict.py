import torch
import torch.nn.functional as F
import timm

from torchvision import transforms
from PIL import Image

MODEL_PATH = "models/agrogpt_model.pth"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# load model
def load_model():

    checkpoint = torch.load(
        MODEL_PATH,
        map_location=DEVICE
    )

    class_names = checkpoint['class_names']

    model = timm.create_model(
        'efficientnet_b0',
        pretrained=False,
        num_classes=len(class_names)
    )

    model.load_state_dict(
        checkpoint['model_state_dict']
    )

    model.to(DEVICE)

    model.eval()

    return model, class_names


model, class_names = load_model()


# transforms
transform = transforms.Compose([

    transforms.Resize((224, 224)),

    transforms.ToTensor(),

    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])


# prediction function
def predict(image_path, crop_name=None, top_k=3):

    image = Image.open(image_path).convert("RGB")

    img = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():

        outputs = model(img)

        probs = F.softmax(outputs, dim=1)[0]

    boosted_results = []

    for idx, class_name in enumerate(class_names):

        score = probs[idx].item()

        
        # strict crop-aware filtering
        if crop_name:
            if crop_name.lower() not in class_name.lower():
                continue

        boosted_results.append({

            "class": class_name,

            "confidence": score * 100,

            "class_idx": idx,

            "tensor": img,

            "model": model
        })

    if len(boosted_results) == 0:
        return [{
        "class": "No matching crop class found",
        "confidence": 0,
        "class_idx": -1,
        "tensor": img,
        "model": model
    }], model  
      
    boosted_results = sorted(

        boosted_results,

        key=lambda x: x["confidence"],

        reverse=True
    )

    return boosted_results[:top_k], model


def predict_image(image_path, crop_name=None):

    results, model = predict(

        image_path,

        crop_name=crop_name
    )

    return results