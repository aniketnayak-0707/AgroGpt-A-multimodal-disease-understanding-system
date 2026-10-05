from core.predict import predict_image

from core.gradcam import (
    generate_gradcam,
    overlay_gradcam
)

from core.knowledge import get_disease_info


def analyze_plant_image(image_path, crop_name=None):

    prediction = predict_image(
        image_path,
        crop_name
    )[0]

    disease_name = prediction["class"].replace(
        "_",
        " "
    ).title()

    confidence = prediction["confidence"]

    class_idx = prediction["class_idx"]

    image_tensor = prediction["tensor"]

    model = prediction["model"]

    # disease information
    disease_info = get_disease_info(
        disease_name
    )

    # gradcam matrix
    cam = generate_gradcam(
        model,
        image_tensor,
        class_idx
    )

    # save gradcam image
    gradcam_path = overlay_gradcam(
        image_path,
        cam
    )

    return {

        "disease": disease_name,

        "confidence": round(
            confidence ,
            2
        ),

        "description": disease_info.get(
            "description",
            "Not available"
        ),

        "cause": disease_info.get(
            "cause",
            "Not available"
        ),

        "remedy": disease_info.get(
            "remedy",
            "Not available"
        ),

        "prevention": disease_info.get(
            "prevention",
            "Not available"
        ),

        "gradcam": gradcam_path
    }