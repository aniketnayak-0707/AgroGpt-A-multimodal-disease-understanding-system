import os
import random
from PIL import Image

BASE_PATH = "raw"

# Minimum recommended images per class
MIN_IMAGES = 50


def verify_classification_dataset(dataset_path, dataset_name):
    print(f"\n{'='*50}")
    print(f"DATASET: {dataset_name}")
    print(f"{'='*50}")

    if not os.path.exists(dataset_path):
        print("Dataset not found!")
        return

    classes = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
    
    print(f"Total classes: {len(classes)}")

    for cls in classes:
        cls_path = os.path.join(dataset_path, cls)
        images = os.listdir(cls_path)

        print(f"\n🔹 Class: {cls}")
        print(f"   Images: {len(images)}")

        if len(images) == 0:
            print(" Empty folder!")
            continue

        if len(images) < MIN_IMAGES:
            print(" Too few images (<50)")

        # Random sample check
        samples = random.sample(images, min(5, len(images)))

        for img_name in samples:
            img_path = os.path.join(cls_path, img_name)
            try:
                img = Image.open(img_path)
                img.verify()
            except:
                print(f" Corrupt image: {img_path}")


def verify_crop_datasets():
    crop_folders = ["cotton", "maize", "mango", "rice"]

    for crop in crop_folders:
        path = os.path.join(BASE_PATH, crop)
        verify_classification_dataset(path, crop)


def verify_plantvillage():
    path = os.path.join(BASE_PATH, "plantvillage")
    verify_classification_dataset(path, "plantvillage")


def verify_plantdoc():
    print(f"\n{'='*50}")
    print("DATASET: plantdoc (YOLO format)")
    print(f"{'='*50}")

    base = os.path.join(BASE_PATH, "plantdoc")

    images_train = os.path.join(base, "images", "train")
    images_val = os.path.join(base, "images", "val")

    labels_train = os.path.join(base, "labels", "train")
    labels_val = os.path.join(base, "labels", "val")

    for split_name, img_path, lbl_path in [
        ("train", images_train, labels_train),
        ("val", images_val, labels_val),
    ]:
        print(f"\n🔹 Split: {split_name}")

        if not os.path.exists(img_path):
            print(" Images folder missing")
            continue

        img_files = os.listdir(img_path)
        lbl_files = os.listdir(lbl_path) if os.path.exists(lbl_path) else []

        print(f"   Images: {len(img_files)}")
        print(f"   Labels: {len(lbl_files)}")

        if len(img_files) != len(lbl_files):
            print(" Mismatch between images and labels")

        # Check few samples
        samples = random.sample(img_files, min(5, len(img_files)))

        for img_name in samples:
            img_path_full = os.path.join(img_path, img_name)
            try:
                img = Image.open(img_path_full)
                img.verify()
            except:
                print(f" Corrupt image: {img_path_full}")


def main():
    print("\n STARTING FULL DATASET VERIFICATION...\n")

    verify_crop_datasets()
    verify_plantvillage()
    verify_plantdoc()

    print("\nVERIFICATION COMPLETE")


if __name__ == "__main__":
    main()