import os
BASE_PATH = "data/raw"
def rename(dataset_name, mapping):
    path = os.path.join(BASE_PATH, dataset_name)
    if not os.path.exists(path):
        print(f"{dataset_name} not found")
        return

    print(f"\nProcessing: {dataset_name}")
    for folder in os.listdir(path):
        old_path = os.path.join(path, folder)
        if not os.path.isdir(old_path):
            continue

        new_name = mapping.get(folder)
        if new_name:
            new_path = os.path.join(path, new_name)
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
                print(f"Renamed: {folder} → {new_name}")
            else:
                print(f"Skipped (exists): {new_name}")
        else:
            print(f"Skipped: {folder}")

#RICE
rice_map = {
    "Bacterial Leaf Blight": "rice___bacterial_leaf_blight",
    "Brown Spot": "rice___brown_spot",
    "Leaf Blast": "rice___blast",
    "Leaf scald": "rice___leaf_scald",
    "Sheath Blight": "rice___sheath_blight",
    "Healthy Rice Leaf": "rice___healthy"}

#WHEAT
wheat_map = {
    "Brown rust": "wheat___brown_rust",
    "Yellow rust": "wheat___yellow_rust",
    "Loose Smut": "wheat___loose_smut",
    "Septoria": "wheat___septoria",
    "Healthy": "wheat___healthy"}

#MANGO
mango_map = {
    "Anthracnose": "mango___anthracnose",
    "Bacterial Canker": "mango___bacterial_canker",
    "Cutting Weevil": "mango___cutting_weevil",
    "Die Back": "mango___die_back",
    "Gall Midge": "mango___gall_midge",
    "Healthy": "mango___healthy",
    "Powdery Mildew": "mango___powdery_mildew",
    "Sooty Mould": "mango___sooty_mould"
  }

#MAIZE
maize_map = {
    "Blight": "maize___blight",
    "Common_Rust": "maize___rust",
    "Gray_Leaf_Spot": "maize___gray_leaf_spot",
    "Healthy": "maize___healthy"}

#PLANTVILLAGE
plantvillage_map = {
    "Pepper__bell___Bacterial_spot": "pepper___bacterial_spot",
    "Pepper__bell___healthy": "pepper___healthy",

    "Potato___Early_blight": "potato___early_blight",
    "Potato___Late_blight": "potato___late_blight",
    "Potato___healthy": "potato___healthy",

    "Tomato_Bacterial_spot": "tomato___bacterial_spot",
    "Tomato_Early_blight": "tomato___early_blight",
    "Tomato_Late_blight": "tomato___late_blight",
    "Tomato_healthy": "tomato___healthy",

    "Tomato_Leaf_Mold": "tomato___mold",
    "Tomato_Septoria_leaf_spot": "tomato___septoria_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite": "tomato___spider_mites",

    "Tomato__Target_Spot": "tomato___target_spot",
    "Tomato__Tomato_mosaic_virus": "tomato___mosaic_virus",
    "Tomato__Tomato_YellowLeaf__Curl_Virus": "tomato___yellow_leaf_curl_virus",}
#RUN ALL
rename("rice", rice_map)
rename("wheat", wheat_map)
rename("mango", mango_map)
rename("maize", maize_map)
rename("plantvillage", plantvillage_map)
print("\nALL RENAMING DONE")