from core.pipeline import run_pipeline
import json
def main():
    print("\nAgroGPT\n")
    image_path = input("Enter image path: ").strip().replace('"', '').replace("'", "")
    print("\nSelect Crop:")
    print("[auto] Auto Detect")
    print("[tomato, potato, rice, mango, apple, grape, maize, wheat, pepper]")
    print("[other] Not in dataset")
    selected_crop = input("Crop (default=auto): ").strip().lower()
    if selected_crop == "":
        selected_crop = "auto"

    result = run_pipeline(image_path, selected_crop)
    print("\nRESULT\n")
    print(json.dumps(result, indent=4))
    print("\nGradCAM saved at:", result["gradcam"])

if __name__ == "__main__":
    main()