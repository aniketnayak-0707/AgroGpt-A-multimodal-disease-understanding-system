import os
import time

import torch
import cv2
import numpy as np


def generate_gradcam(model, image_tensor, class_idx):

    gradients = []

    activations = []

    def backward_hook(module, grad_input, grad_output):

        gradients.append(grad_output[0])

    def forward_hook(module, input, output):

        activations.append(output)

    # EfficientNet last conv layer
    target_layer = model.conv_head

    forward_handle = target_layer.register_forward_hook(
        forward_hook
    )

    backward_handle = target_layer.register_backward_hook(
        backward_hook
    )

    output = model(image_tensor)

    model.zero_grad()

    loss = output[0, class_idx]

    loss.backward()

    grads = gradients[0].cpu().data.numpy()[0]

    acts = activations[0].cpu().data.numpy()[0]

    weights = np.mean(grads, axis=(1, 2))

    cam = np.zeros(acts.shape[1:], dtype=np.float32)

    for i, w in enumerate(weights):

        cam += w * acts[i]

    cam = np.maximum(cam, 0)

    cam = cv2.resize(cam, (224, 224))

    cam = cam - np.min(cam)

    cam = cam / np.max(cam)

    # remove hooks
    forward_handle.remove()

    backward_handle.remove()

    return cam


def overlay_gradcam(image_path, cam):

    img = cv2.imread(image_path)

    img = cv2.resize(img, (224, 224))

    heatmap = cv2.applyColorMap(

        np.uint8(255 * cam),

        cv2.COLORMAP_JET
    )

    overlay = heatmap * 0.4 + img

    # unique filename
    filename = f"gradcam_{int(time.time())}.jpg"

    os.makedirs("outputs", exist_ok=True)

    output_path = os.path.join(
        "outputs",
        filename
    )

    cv2.imwrite(output_path, overlay)

    return f"/outputs/{filename}"