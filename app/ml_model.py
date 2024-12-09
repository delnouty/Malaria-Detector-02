import tensorflow as tf
import numpy as np
from PIL import Image
import os

class MalariaDetector:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'malaria_model.keras')
        self.model = tf.keras.models.load_model(model_path)
        # Récupérer la forme d'entrée attendue par le modèle
        self.input_shape = self.model.input_shape[1:3]  # (height, width)

    def preprocess_image(self, image_path):
        try:
            # Charger et prétraiter l'image
            img = Image.open(image_path)
            # Convertir en RGB si nécessaire
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # Redimensionner selon la taille attendue par le modèle
            img = img.resize(self.input_shape)
            # Convertir en array et normaliser
            img_array = np.array(img) / 255.0
            # Ajouter la dimension du batch
            img_array = np.expand_dims(img_array, axis=0)
            return img_array
        except Exception as e:
            raise Exception(f"Erreur lors du prétraitement de l'image : {str(e)}")

    def predict(self, image_path):
        try:
            img_array = self.preprocess_image(image_path)
            prediction = self.model.predict(img_array, verbose=0)  # Désactiver les logs de prédiction
            probability = float(prediction[0][0])
            
            result = {
                'probability': round(probability * 100, 2),
                'prediction': 'Pas de paludisme détecté' if probability > 0.5 else 'Paludisme détecté',
                'status': 'negative' if probability > 0.5 else 'positive'
            }
            return result
        except Exception as e:
            return {'error': str(e)} 