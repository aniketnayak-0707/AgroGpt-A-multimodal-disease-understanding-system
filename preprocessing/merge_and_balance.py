import os
import shutil
import random
import hashlib
from tqdm import tqdm
#CONFIG
RAW_PATH = "data/raw"
PLANTDOC_PATH = "data/processed/plantdoc_classification"
OUTPUT_PATH = "data/processed/final_dataset"
MIN_IMAGES = 100
MAX_IMAGES = 400
DATASETS = [
    PLANTDOC_PATH,
    os.path.join(RAW_PATH, "rice"),
    os.path.join(RAW_PATH, "wheat"),
    os.path.join(RAW_PATH, "mango"),
    os.path.join(RAW_PATH, "maize"),
    os.path.join(RAW_PATH, "plantvillage")]
#UTILS
def get_images(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))]

def hash_image(path):
    try:
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def copy_images(images, dest_folder, existing_hashes):
    os.makedirs(dest_folder, exist_ok=True)
    count = 0
    for img in images:
        h = hash_image(img)
        if h is None or h in existing_hashes:
            continue

        existing_hashes.add(h)
        filename = f"{count}_{os.path.basename(img)}"
        shutil.copy(img, os.path.join(dest_folder, filename))
        count += 1

    return count
#COLLECT
class_data = {}
merge_log = {}
print("\nCOLLECTING DATA\n")

for dataset in DATASETS:
    if not os.path.exists(dataset):
        continue

    dataset_name = os.path.basename(dataset)
    print(f"Reading: {dataset_name}")

    for cls in os.listdir(dataset):
        cls_path = os.path.join(dataset, cls)
        if not os.path.isdir(cls_path):
            continue

        images = get_images(cls_path)
        if len(images) == 0:
            continue

        if cls not in class_data:
            class_data[cls] = []
            merge_log[cls] = []

        class_data[cls].extend(images)
        merge_log[cls].append(dataset_name)

#MERGE
print("\nMERGING\n")
if os.path.exists(OUTPUT_PATH):
    shutil.rmtree(OUTPUT_PATH)

os.makedirs(OUTPUT_PATH, exist_ok=True)
final_counts = {}
removed_classes = []
for cls, images in class_data.items():

    if len(images) < MIN_IMAGES:
        removed_classes.append((cls, "below_min_before_merge"))
        print(f"Skipping {cls} (<{MIN_IMAGES})")
        continue

    random.shuffle(images)
    if len(images) > MAX_IMAGES:
        images = images[:MAX_IMAGES]

    dest = os.path.join(OUTPUT_PATH, cls)
    existing_hashes = set()
    copied = copy_images(images, dest, existing_hashes)
    if copied >= MIN_IMAGES:
        final_counts[cls] = copied
        print(f"{cls} → {copied}")
    else:
        shutil.rmtree(dest)
        removed_classes.append((cls, "below_min_after_dedup"))
        print(f"Removed {cls} after dedup (<{MIN_IMAGES})")

#SUMMARY
print("\nFINAL DATASET SUMMARY\n")
print(f"Total Classes: {len(final_counts)}")
for cls, count in sorted(final_counts.items()):
    print(f"{cls}: {count}")

#MERGE DETAILS
print("\nMERGE DETAILS\n")
for cls, sources in merge_log.items():
    if cls in final_counts:
        print(f"{cls} ← merged from {list(set(sources))}")

#REMOVED CLASSES
print("\nREMOVED CLASSES\n")
for cls, reason in removed_classes:
    print(f"{cls} → {reason}")

print("\nDONE")