# 🌱 AGRO-GPT: A Multimodal Agricultural Disease Understanding System

<p align="center">
  <b>AI-powered plant disease detection, explainability, and agricultural assistance</b>
</p>

<p align="center">
  <a href="https://agro-gpt-a-multimodal-disease-under.vercel.app/">
    <img src="https://img.shields.io/badge/Live%20Demo-AGRO--GPT-success?style=for-the-badge" alt="Live Demo">
  </a>
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/PyTorch-Deep%20Learning-ee4c2c?style=for-the-badge&logo=pytorch" alt="PyTorch">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react" alt="React">
</p>

---

## 📌 Overview

**AGRO-GPT** is an AI-powered agricultural disease understanding system designed to assist in the early identification of plant diseases from leaf images.

The system combines **Deep Learning, Explainable AI, uncertainty-aware prediction, and an agricultural knowledge engine** into a single web-based platform.

Users can upload a plant leaf image, select the crop, and receive:

- 🌿 Predicted plant disease
- 📊 Prediction confidence
- 🔍 Grad-CAM explainability heatmap
- 🧪 Disease description
- 💡 Possible causes
- 💊 Recommended remedies
- 🛡️ Prevention measures
- 🌾 Agricultural recommendations

The system uses **EfficientNet-B0 with transfer learning** for disease classification and **Grad-CAM** to visualize the regions of the leaf that influenced the model's prediction.

---

## 🚀 Live Demo

**Frontend:**  
https://agro-gpt-a-multimodal-disease-under.vercel.app/

The frontend is deployed on **Vercel**, while the backend is deployed using **Hugging Face Spaces**.

---

## 🎯 Problem Statement

Plant disease detection is traditionally dependent on manual inspection and agricultural experts. This approach can be time-consuming, expensive, and difficult to access in rural areas.

Additionally, many AI-based disease detection systems behave as **black-box models**, providing predictions without explaining why a particular disease was detected.

AGRO-GPT addresses these challenges by combining:

1. Automated disease classification
2. Explainable AI
3. Confidence-aware prediction
4. Agricultural recommendations
5. Cloud-based accessibility

The goal is to provide a practical and transparent AI-assisted system for agricultural disease understanding.

---

## ✨ Key Features

### 🌿 Plant Disease Detection

Uses a fine-tuned **EfficientNet-B0** model to classify plant leaf images into **42 disease categories**.

### 🔍 Explainable AI with Grad-CAM

Grad-CAM generates heatmaps highlighting the regions of the leaf that contributed most to the model's prediction.

This helps users understand the visual basis of the prediction instead of receiving only a disease label.

### 📊 Uncertainty-Aware Prediction

The system analyzes prediction confidence to identify uncertain predictions and reduce the risk of presenting unreliable predictions with excessive confidence.

### 🌾 Crop-Aware Prediction

Users can select the crop type before prediction, allowing the system to apply crop-aware filtering during disease classification.

### 🧠 Agricultural Knowledge Engine

After identifying a disease, the knowledge engine provides relevant agricultural information, including:

- Disease description
- Causes
- Remedies
- Prevention
- Agricultural recommendations

### ⚡ Real-Time Web Application

The system provides an interactive web interface where users can upload leaf images and receive predictions and recommendations.

### ☁️ Cloud Deployment

The application is deployed using:

- **Vercel** – Frontend
- **Hugging Face Spaces** – Backend

---

## 🧠 Machine Learning Model

### EfficientNet-B0

AGRO-GPT uses **EfficientNet-B0 pretrained on ImageNet** and fine-tuned for agricultural disease classification.

EfficientNet-B0 was selected because it provides a good balance between:

- Classification performance
- Computational efficiency
- Model size
- Inference speed
- Suitability for future edge/mobile deployment

### Model Configuration

| Parameter | Value |
|---|---|
| Architecture | EfficientNet-B0 |
| Pretrained Weights | ImageNet |
| Number of Classes | 42 |
| Input Size | 224 × 224 |
| Optimizer | Adam |
| Batch Size | 32 |
| Learning Rate | 0.001 |
| Epochs | 25 |
| Loss Function | Cross-Entropy |
| Explainability | Grad-CAM |

---

## 📊 Dataset

The project combines multiple agricultural image datasets, including:

- **PlantVillage**
- **PlantDoc**
- Crop-specific disease datasets

The final dataset contains:

- **14,836 images**
- **42 disease categories**
- Healthy and diseased plant leaves
- Images captured under different lighting and background conditions

### Dataset Preparation

The preprocessing pipeline includes:

- Duplicate removal
- Corrupted image removal
- Class mapping
- Image resizing
- Normalization
- Data augmentation
- Dataset balancing
- Stratified train/validation/test splitting

Images are resized to **224 × 224 pixels** to match the EfficientNet-B0 input requirements.

### Data Augmentation

The training pipeline uses:

- Rotation
- Horizontal flipping
- Brightness adjustment
- Zoom transformation
- Normalization

These techniques improve robustness against variations in leaf orientation, lighting, scale, and environmental conditions.

---

## 🔬 Exploratory Data Analysis

EDA was performed to understand the quality and distribution of the agricultural dataset.

The analysis included:

- Class distribution
- Crop-wise distribution
- Duplicate detection
- Feature distribution
- PCA visualization
- t-SNE visualization
- Analysis of image quality and background variation

The t-SNE analysis showed that some visually similar diseases form overlapping feature clusters, demonstrating the difficulty of fine-grained disease classification.

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      User            │
                    │  Plant Leaf Image    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ React + Vite         │
                    │ Frontend             │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ FastAPI Backend      │
                    │ Image Processing     │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │ Preprocessing        │
                    │ 224×224 + Normalize  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ EfficientNet-B0      │
                    │ Disease Classifier   │
                    └──────────┬───────────┘
                               │
                  ┌────────────┴────────────┐
                  ▼                         ▼
        ┌──────────────────┐       ┌──────────────────┐
        │ Confidence /     │       │ Grad-CAM         │
        │ Uncertainty      │       │ Explainability   │
        └────────┬─────────┘       └────────┬─────────┘
                 │                          │
                 └────────────┬─────────────┘
                              ▼
                  ┌─────────────────────────┐
                  │ Agricultural Knowledge │
                  │ Engine                  │
                  └────────────┬────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Final Result         │
                    │ Disease + Confidence│
                    │ Heatmap + Advice     │
                    └──────────────────────┘
