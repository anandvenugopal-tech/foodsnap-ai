import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import os

model = load_model('models/food-19.keras')

class_names = sorted(os.listdir('data/food-20/train'))

def preprocess(img):
    img = img.resize((224, 224))
    img = img.convert("RGB")
    img = np.array(img)
    return np.expand_dims(img, axis = 0)

def predict_food(image):
    img = preprocess(image)
    pred = model.predict(img)[0]
    class_id = np.argmax(pred)
    food_name = class_names[class_id]
    confidence = pred[class_id]
    return food_name, confidence

