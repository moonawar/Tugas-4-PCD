import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import json

TRANSLATION_MAP = {
    "bus": "Bus",
    "car": "Mobil",
    "bird": "Burung",
    "cat": "Kucing",
    "deer": "Rusa",
    "dog": "Anjing",
    "frog": "Katak",
    "horse": "Kuda",
    "ship": "Kapal",
    "truck": "Truk"
}

def classify_image(image_path):
    # Load model
    model = load_model('../model/cnn_model.h5')

    # Load class labels
    with open('../model/cnn_class_labels.json', 'r') as f:
        class_indices = json.load(f)
    
    # Load image
    img = image.load_img(image_path, target_size=(32, 32))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    # Classify image
    prediction = model.predict(img_array)
    predicted_class = class_indices[np.argmax(prediction)]

    predicted_class = TRANSLATION_MAP[predicted_class]

    return predicted_class