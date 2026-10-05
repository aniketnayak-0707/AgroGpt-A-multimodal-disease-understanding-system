import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# =========================
# CONFIG
# =========================
DATASET_PATH = "data/processed/final_dataset"
OUTPUT_PATH = "outputs/dataplots"

os.makedirs(OUTPUT_PATH, exist_ok=True)

print("\nSTARTING FINAL DATASET EDA...\n")

# =========================
# LOAD DATA
# =========================
class_counts = {}
X = []
y = []

class_to_idx = {}

img_size = 64  # small for PCA/TSNE speed

for idx, class_name in enumerate(sorted(os.listdir(DATASET_PATH))):
    class_path = os.path.join(DATASET_PATH, class_name)

    if not os.path.isdir(class_path):
        continue

    class_to_idx[class_name] = idx

    images = os.listdir(class_path)
    class_counts[class_name] = len(images)

    for img_name in images:
        img_path = os.path.join(class_path, img_name)

        try:
            img = cv2.imread(img_path)
            img = cv2.resize(img, (img_size, img_size))
            img = img.flatten()

            X.append(img)
            y.append(idx)

        except:
            continue

print("DATA LOADED\n")

X = np.array(X)
y = np.array(y)

# =========================
# SUMMARY
# =========================
print("CLASS-WISE IMAGE COUNT:\n")

for cls, count in class_counts.items():
    print(f"{cls}: {count}")

total_images = sum(class_counts.values())
max_images = max(class_counts.values())
min_images = min(class_counts.values())
imbalance_ratio = max_images / min_images

print("\nDATASET SUMMARY")
print(f"Total classes: {len(class_counts)}")
print(f"Total images: {total_images}")
print(f"Max images: {max_images}")
print(f"Min images: {min_images}")
print(f"Imbalance ratio: {imbalance_ratio}")

# =========================
# BAR PLOT - IMAGES PER CLASS
# =========================
plt.figure(figsize=(12,6))
plt.bar(range(len(class_counts)), list(class_counts.values()))
plt.title("Images per Class")
plt.xlabel("Class Index")
plt.ylabel("Image Count")
plt.savefig(f"{OUTPUT_PATH}/images_per_class.png")
plt.close()

# =========================
# BOX PLOT
# =========================
plt.figure()
plt.boxplot(list(class_counts.values()))
plt.title("Box Plot of Class Distribution")
plt.savefig(f"{OUTPUT_PATH}/boxplot.png")
plt.close()

# =========================
# HISTOGRAM DISTRIBUTION
# =========================
plt.figure()
plt.hist(list(class_counts.values()), bins=20)
plt.title("Class Distribution")
plt.xlabel("Images per class")
plt.ylabel("Frequency")
plt.savefig(f"{OUTPUT_PATH}/distribution.png")
plt.close()

# =========================
# PIE CHART (TOP CLASSES)
# =========================
sorted_classes = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)

top_n = 10
top_classes = sorted_classes[:top_n]

labels = [cls for cls, _ in top_classes]
sizes = [count for _, count in top_classes]
sizes_percent = [(s / total_images) * 100 for s in sizes]

plt.figure(figsize=(8,8))
plt.pie(sizes_percent, labels=labels, autopct='%1.1f%%')
plt.title("Dataset Composition (%)")
plt.savefig(f"{OUTPUT_PATH}/composition_pie_chart.png")
plt.close()

# =========================
# PCA
# =========================
print("Running PCA...")

sample_size = 2000

if len(X) > sample_size:
    idx = np.random.choice(len(X), sample_size, replace=False)
    X_sample = X[idx]
    y_sample = y[idx]
else:
    X_sample = X
    y_sample = y

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_sample)

plt.figure(figsize=(8,6))
plt.scatter(X_pca[:,0], X_pca[:,1], c=y_sample, s=5)
plt.title("PCA Cluster Plot")
plt.savefig(f"{OUTPUT_PATH}/pca_plot.png")
plt.close()

# =========================
# TSNE
# =========================
print("Running TSNE...")

sample_size = 2000

if len(X) > sample_size:
    idx = np.random.choice(len(X), sample_size, replace=False)
    X_sample = X[idx]
    y_sample = y[idx]
else:
    X_sample = X
    y_sample = y

tsne = TSNE(n_components=2, random_state=42, perplexity=30)
X_tsne = tsne.fit_transform(X_sample)

plt.figure(figsize=(8,6))
plt.scatter(X_tsne[:,0], X_tsne[:,1], c=y_sample, s=5)
plt.title("t-SNE Plot")
plt.savefig(f"{OUTPUT_PATH}/tsne_plot.png")
plt.close()

print("\nEDA COMPLETE")
print(f"Plots saved in: {OUTPUT_PATH}\n")