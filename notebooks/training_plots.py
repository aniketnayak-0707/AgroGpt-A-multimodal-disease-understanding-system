import os
import matplotlib.pyplot as plt
import numpy as np
import torch
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import timm

# PATH
OUTPUT_PATH = "outputs/train_plots"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# PASTE YOUR VALUES HERE

train_losses = [1.4286, 0.4700, 0.2945, 0.1993, 0.1459, 0.1004, 0.0914, 0.0687, 0.0591, 0.0491]
val_losses   = [0.6021, 0.4133, 0.3599, 0.3115, 0.3198, 0.2961, 0.2853, 0.2753, 0.2838, 0.2995]
val_acc      = [0.8150, 0.8675, 0.8918, 0.9093, 0.9088, 0.9147, 0.9192, 0.9250, 0.9241, 0.9308]

epochs = list(range(1, len(train_losses)+1))

# 1. ADVANCED LOSS CURVE

plt.figure(figsize=(10,6))

plt.plot(epochs, train_losses, marker='o', linewidth=2, label="Train Loss")
plt.plot(epochs, val_losses, marker='s', linewidth=2, label="Validation Loss")

# highlight best epoch
best_epoch = np.argmin(val_losses) + 1
plt.axvline(best_epoch, linestyle='--', label=f"Best Epoch: {best_epoch}")

plt.title("Training vs Validation Loss (Advanced View)")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.grid(alpha=0.3)

plt.savefig(f"{OUTPUT_PATH}/loss_curve.png")
plt.close()

# 2. ACCURACY TREND + SMOOTHING

def moving_avg(x, k=3):
    return np.convolve(x, np.ones(k)/k, mode='valid')

plt.figure(figsize=(10,6))

plt.plot(epochs, val_acc, marker='o', linewidth=2, label="Raw Accuracy")

smooth_acc = moving_avg(val_acc)
plt.plot(range(2, len(smooth_acc)+2), smooth_acc, linewidth=3, label="Smoothed Accuracy")

plt.title("Validation Accuracy Trend (Smoothed)")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(alpha=0.3)

plt.savefig(f"{OUTPUT_PATH}/accuracy_trend.png")
plt.close()

# 3. GENERALIZATION GAP 
gap = np.array(val_losses) - np.array(train_losses)

plt.figure(figsize=(10,6))

plt.plot(epochs, gap, marker='o', linewidth=2)
plt.axhline(0, linestyle='--')

plt.title("Generalization Gap (Val Loss - Train Loss)")
plt.xlabel("Epoch")
plt.ylabel("Gap")
plt.grid(alpha=0.3)

plt.savefig(f"{OUTPUT_PATH}/generalization_gap.png")
plt.close()

# 4. LOSS vs ACCURACY COMBINED 
fig, ax1 = plt.subplots(figsize=(10,6))

ax1.plot(epochs, val_losses, marker='o', label="Val Loss")
ax1.set_xlabel("Epoch")
ax1.set_ylabel("Loss")

ax2 = ax1.twinx()
ax2.plot(epochs, val_acc, marker='s', label="Val Accuracy")
ax2.set_ylabel("Accuracy")

plt.title("Loss vs Accuracy Relationship")

fig.tight_layout()
plt.savefig(f"{OUTPUT_PATH}/loss_vs_accuracy.png")
plt.close()

print("\nTraining plots saved at:", OUTPUT_PATH)

print("\nGenerating Confusion Matrix...\n")

MODEL_PATH = "models/agrogpt_model.pth"   # change if different
DATASET_PATH = "data/final_dataset_split"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# TRANSFORM 
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# LOAD TEST DATA

test_dataset = datasets.ImageFolder(
    os.path.join(DATASET_PATH, "test"),
    transform=transform
)

test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

class_names = test_dataset.classes

# LOAD MODEL

checkpoint = torch.load(MODEL_PATH, map_location=device)

model = timm.create_model(
    'efficientnet_b0',
    pretrained=False,
    num_classes=len(checkpoint['class_names'])
)

model.load_state_dict(checkpoint['model_state_dict'])
model = model.to(device)
model.eval()

# PREDICTIONS
y_true = []
y_pred = []

with torch.no_grad():
    for images, labels in test_loader:
        images = images.to(device)

        outputs = model(images)
        _, preds = torch.max(outputs, 1)

        y_true.extend(labels.numpy())
        y_pred.extend(preds.cpu().numpy())

print("Predictions completed")

# CONFUSION MATRIX
cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(16,12))
sns.heatmap(cm, cmap="viridis")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig(f"{OUTPUT_PATH}/confusion_matrix.png")
plt.close()

# NORMALIZED CONFUSION MATRIX
cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

plt.figure(figsize=(16,12))
sns.heatmap(cm_norm, cmap="viridis")
plt.title("Normalized Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig(f"{OUTPUT_PATH}/confusion_matrix_normalized.png")
plt.close()
# CLASSIFICATION REPORT
report = classification_report(y_true, y_pred, target_names=class_names)
print("\nCLASSIFICATION REPORT:\n")
print(report)
with open(f"{OUTPUT_PATH}/classification_report.txt", "w") as f:
    f.write(report)

print("\nConfusion matrix + report saved in:", OUTPUT_PATH)