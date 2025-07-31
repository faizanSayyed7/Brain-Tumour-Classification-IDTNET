import os
import time
from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
import numpy as np
from utils import preprocess_image, allowed_file, create_demo_prediction
import tensorflow as tf

app = Flask(__name__)
app.secret_key = "change-this-key"
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

MODEL_CONFIG = {
    'IDTNet': {
        'filename': 'idtnet_model.keras',
        'description': 'Inception-Dense-Transition hybrid model',
        'accuracy': 98.13,
        'parameters': '54M',
        'icon': 'fa-brain'
    },
    'VGG16': {
        'filename': 'myvgg_model.keras',
        'description': 'Visual Geometry Group 16-layer model',
        'accuracy': 92.80,
        'parameters': '138M',
        'icon': 'fa-layer-group'
    },
    'DenseNet121': {
        'filename': 'mydensenet_model.keras',
        'description': 'Densely connected convolutional networks',
        'accuracy': 96.10,
        'parameters': '28M',
        'icon': 'fa-project-diagram'
    },
    'InceptionV1': {
        'filename': 'myGoogLeNet_model.keras',
        'description': "Google's Inception architecture",
        'accuracy': 94.20,
        'parameters': '23M',
        'icon': 'fa-sitemap'
    }
}

CLASS_LABELS = ['Glioma', 'Meningioma', 'No Tumor', 'Pituitary']

# Load models at startup if possible
def load_all_models():
    models = {}
    try:
        models['IDTNet'] = tf.keras.models.load_model('models/idtnet_model.keras')
        models['VGG16'] = tf.keras.models.load_model('models/myvgg_model.keras')
        models['DenseNet121'] = tf.keras.models.load_model('models/mydensenet_model.keras')
        models['InceptionV1'] = tf.keras.models.load_model('models/myGoogLeNet_model.keras')
        return models, True
    except Exception as e:
        print(f"Model loading failed, using demo mode: {e}")
        return {}, False

models, models_loaded = load_all_models()

@app.route('/')
def index():
    return render_template('index.html',
                           model_config=MODEL_CONFIG,
                           models_loaded=models_loaded)

@app.route('/classify', methods=['POST'])
def classify_tumor():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file format. Please upload JPEG, PNG, or DICOM files.'}), 400

    filename = secure_filename(file.filename)
    timestamp = str(int(time.time()))
    filename = f"{timestamp}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    image_url = url_for('static', filename=f'uploads/{filename}')
    predictions = []

    if models_loaded:
        img_array = preprocess_image(filepath)
        for model_name in MODEL_CONFIG.keys():
            start_time = time.time()
            model = models[model_name]
            preds = model.predict(img_array, verbose=0)[0]
            processing_time = int((time.time() - start_time) * 1000)
            class_idx = int(np.argmax(preds))
            confidence = float(preds[class_idx]) * 100
            predictions.append({
                'model': model_name,
                'prediction': CLASS_LABELS[class_idx],
                'confidence': f"{confidence:.2f}",
                'processing_time': f"{processing_time}ms",
                'accuracy': MODEL_CONFIG[model_name]['accuracy'],
                'icon': MODEL_CONFIG[model_name]['icon']
            })
    else:
        predictions = create_demo_prediction(MODEL_CONFIG, CLASS_LABELS)

    return jsonify({
        'success': True,
        'predictions': predictions,
        'image_url': image_url,
        'demo_mode': not models_loaded
    })

if __name__ == '__main__':
    app.run(debug=True)
