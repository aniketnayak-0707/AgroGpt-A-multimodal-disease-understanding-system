from core.predict import predict, transform
from core.gradcam import generate_gradcam, overlay_gradcam
from core.knowledge import get_disease_info
from PIL import Image

# Helpers
def get_crop(class_name):
    return class_name.split("___")[0]

def format_name(class_name):
    crop, disease = class_name.split("___")
    return f"{crop.capitalize()} - {disease.replace('_',' ').capitalize()}"

def filter_by_crop(predictions, selected_crop):
    return [
        p for p in predictions
        if get_crop(p["class"]) == selected_crop.lower()
    ]

# Main Pipeline
def run_pipeline(image_path, selected_crop="auto"):
    #Prediction
    predictions, model = predict(image_path)
    if len(predictions) == 0:
        return {"status": "error", "message": "No predictions found"}
    #Crop Filtering
    if selected_crop == "auto":
        crop_scores = {}
        for p in predictions:
            crop = get_crop(p["class"])
            crop_scores[crop] = crop_scores.get(crop, 0) + p["confidence"]
        best_crop = max(crop_scores, key=crop_scores.get)
        filtered_preds = filter_by_crop(predictions, best_crop)

    elif selected_crop == "other":
        filtered_preds = predictions

    else:
        filtered_preds = filter_by_crop(predictions, selected_crop)

        if len(filtered_preds) == 0:
            filtered_preds = predictions  # fallback

    #Final Prediction
    top_preds = filtered_preds[:3]
    final_pred = top_preds[0]["class"]
    confidence = round(top_preds[0]["confidence"], 3)
    # GradCAM
    image = Image.open(image_path).convert("RGB")
    img_tensor = transform(image).unsqueeze(0)
    class_idx = model(img_tensor).argmax().item()
    cam = generate_gradcam(model, img_tensor, class_idx)
    gradcam_path = overlay_gradcam(image_path, cam)
    # Knowledge
    if "healthy" in final_pred:
        disease_info = {
            "crop": get_crop(final_pred).capitalize(),
            "disease": "Healthy",
            "summary": "The plant appears healthy with no visible disease symptoms.",
            "advice": "Maintain proper watering, sunlight, and regular monitoring."
        }
    else:
        disease_info = get_disease_info(final_pred)
    # Final Output 
    return {
        "prediction": format_name(final_pred),
        "confidence": confidence,
        "top_predictions": [
            {
                "name": format_name(p["class"]),
                "confidence": round(p["confidence"], 3)
            }
            for p in top_preds
        ],
        "gradcam": gradcam_path,
        "info": disease_info
    }