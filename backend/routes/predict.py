from fastapi import APIRouter, UploadFile, File, Form
from backend.services.ai_service import analyze_plant_image

import shutil
import os

router = APIRouter()

UPLOAD_DIR = "backend/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/predict")
async def predict(
    file: UploadFile = File(...),
    crop_type: str = Form(None)
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    result = analyze_plant_image(
        file_path,
        crop_type
    )

    return result