import os
import shutil
import random

DATASET_PATH = "data/processed/final_dataset"
OUTPUT_PATH = "data/final_dataset_split"

TRAIN_SPLIT = 0.7
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15

random.seed(42)

def create_dirs():
    for split in ["train", "val", "test"]:
        split_path = os.path.join(OUTPUT_PATH, split)
        os.makedirs(split_path, exist_ok=True)

def split_class(class_name):
    src_path = os.path.join(DATASET_PATH, class_name)

    images = os.listdir(src_path)
    random.shuffle(images)

    total = len(images)
    train_end = int(total * TRAIN_SPLIT)
    val_end = int(total * (TRAIN_SPLIT + VAL_SPLIT))

    splits = {
        "train": images[:train_end],
        "val": images[train_end:val_end],
        "test": images[val_end:]
    }

    for split, imgs in splits.items():
        dest_class_path = os.path.join(OUTPUT_PATH, split, class_name)
        os.makedirs(dest_class_path, exist_ok=True)

        for img in imgs:
            src = os.path.join(src_path, img)
            dst = os.path.join(dest_class_path, img)

            try:
                shutil.copy2(src, dst)
            except:
                continue

    print(f"{class_name} -> train:{len(splits['train'])}, val:{len(splits['val'])}, test:{len(splits['test'])}")

print("\nSTARTING DATASET SPLIT...\n")

create_dirs()

for class_name in os.listdir(DATASET_PATH):
    if os.path.isdir(os.path.join(DATASET_PATH, class_name)):
        split_class(class_name)

print("\nSPLIT COMPLETE")