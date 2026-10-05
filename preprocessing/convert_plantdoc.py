import os
import cv2
import yaml
from tqdm import tqdm
# PATHS
BASE_PATH = "data/raw/plantdoc"
OUTPUT_PATH = "data/processed/plantdoc_classification"
os.makedirs(OUTPUT_PATH, exist_ok=True)
# CLEAN CLASS NAME FUNCTION
def clean_class_name(name):
    name = name.lower()
    name = name.replace("leaf", "").strip()
    # manual normalization
    name = name.replace("bell_pepper", "pepper")
    name = name.replace("corn", "maize")
    name = name.replace("  ", " ")
    name = name.replace(" ", "_")
    # mapping rules
    if "healthy" in name or name in ["tomato", "apple", "cherry", "potato", "grape", "pepper"]:
        plant = name.split("_")[0]
        return f"{plant}___healthy"
    # split plant + disease
    words = name.split("_")
    plant = words[0]
    disease = "_".join(words[1:]) if len(words) > 1 else "healthy"
    # specific fixes
    disease = disease.replace("yellow_virus", "yellow_leaf_curl_virus")
    disease = disease.replace("mosaic_virus", "mosaic_virus")
    disease = disease.replace("two_spotted_spider_mites", "spider_mites")
    disease = disease.replace("gray_leaf_spot", "gray_leaf_spot")
    disease = disease.replace("early_blight", "early_blight")
    disease = disease.replace("late_blight", "late_blight")
    disease = disease.replace("bacterial_spot", "bacterial_spot")
    disease = disease.replace("septoria_leaf_spot", "septoria_leaf_spot")
    disease = disease.replace("scab", "scab")
    disease = disease.replace("rust", "rust")
    disease = disease.replace("black_rot", "black_rot")
    if disease == "":
        disease = "healthy"

    return f"{plant}___{disease}"
# LOAD YAML
yaml_path = os.path.join(BASE_PATH, "dataset.yaml")
with open(yaml_path, "r") as f:
    data = yaml.safe_load(f)

class_map = data["names"]
# YOLO to CROP FUNCTION
def yolo_to_bbox(img_w, img_h, x, y, w, h):
    x1 = int((x - w / 2) * img_w)
    y1 = int((y - h / 2) * img_h)
    x2 = int((x + w / 2) * img_w)
    y2 = int((y + h / 2) * img_h)
    return max(0, x1), max(0, y1), min(img_w, x2), min(img_h, y2)

# PROCESS FUNCTION
def process_split(split):
    img_dir = os.path.join(BASE_PATH, "images", split)
    lbl_dir = os.path.join(BASE_PATH, "labels", split)
    images = os.listdir(img_dir)
    for img_name in tqdm(images, desc=f"Processing {split}"):
        img_path = os.path.join(img_dir, img_name)
        lbl_path = os.path.join(lbl_dir, img_name.replace(".jpg", ".txt").replace(".png", ".txt"))
        if not os.path.exists(lbl_path):
            continue

        img = cv2.imread(img_path)
        if img is None:
            continue

        h, w, _ = img.shape
        with open(lbl_path, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            parts = line.strip().split()
            if len(parts) != 5:
                continue

            class_id, x, y, bw, bh = map(float, parts)
            class_name = class_map[int(class_id)]
            clean_name = clean_class_name(class_name)
            x1, y1, x2, y2 = yolo_to_bbox(w, h, x, y, bw, bh)
            crop = img[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            save_dir = os.path.join(OUTPUT_PATH, clean_name)
            os.makedirs(save_dir, exist_ok=True)
            save_name = f"{img_name.split('.')[0]}_{i}.jpg"
            save_path = os.path.join(save_dir, save_name)
            cv2.imwrite(save_path, crop)

# RUN
if __name__ == "__main__":
    print("Starting PlantDoc Conversion...")
    process_split("train")
    process_split("val")
    print("Conversion Complete.")