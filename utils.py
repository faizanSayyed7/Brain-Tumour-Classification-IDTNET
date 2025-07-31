import os
import cv2
import numpy as np
from PIL import Image
import random

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'dcm', 'dicom'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(filepath):
    """
    Preprocess the input image:
    - Read with OpenCV or PIL
    - Apply bilateral filter
    - Resize to 128x128
    - Convert to RGB
    - Normalize pixel values to [0, 1]
    - Add batch dimension
    """
    try:
        img = cv2.imread(filepath)
        if img is None:
            img = Image.open(filepath).convert('RGB')
            img = np.array(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (128, 128))
        img = img.astype('float32') / 255.0  # Normalization
        img = np.expand_dims(img, axis=0)
        return img
    except Exception as e:
        raise Exception(f"Image preprocessing failed: {str(e)}")

def create_demo_prediction(model_config, class_labels):
    #
    # Generate demo predictions if models aren't loaded
    #
    predictions = []
    demo_results = {
        'IDTNet': {'class': 'Glioma', 'confidence': 96.78},
        'VGG16': {'class': 'Glioma', 'confidence': 85.22},
        'DenseNet121': {'class': 'No Tumor', 'confidence': 82.29},
        'InceptionV1': {'class': 'Glioma', 'confidence': 92.94}
    }
    for model_name, config in model_config.items():
        processing_time = random.randint(154, 441)
        demo_pred = demo_results[model_name]
        predictions.append({
            'model': model_name,
            'prediction': demo_pred['class'],
            'confidence': f"{demo_pred['confidence']:.2f}",
            'processing_time': f"{processing_time}ms",
            'accuracy': config['accuracy'],
            'icon': config['icon']
        })
    return predictions
