import numpy as np
from keras._tf_keras.keras.models import load_model
from keras._tf_keras.keras.preprocessing.image import img_to_array, load_img

class SkinCancerPredictor:
    def __init__(self, model_path, class_labels=["Cancer", "Non_Cancer"], target_size=(224, 224)):
        self.model = load_model(model_path)
        self.class_labels = class_labels
        self.target_size = target_size

        
    def preprocess_image(self, image_path):
        # Load and convert the image to RGB (in case it's grayscale or another format)
        img = load_img(image_path, target_size=self.target_size).convert("RGB")
        img_array = img_to_array(img)
        img_array = img_array / 255.0  # Normalize pixel values to [0, 1]
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        return img_array
    

    def predict(self, image_path):
        # Preprocess image and make prediction
        image_array = self.preprocess_image(image_path)
        prediction = self.model.predict(image_array)[0]  # [0.87] if sigmoid

        print("Raw prediction:", prediction) # [0.87] for example
        print("Shape:", prediction.shape)  # (1,)


        if len(prediction.shape) == 0 or prediction.shape[0] == 1:

            # print("Binary (Cancer or Non-Cancer)")
            # Binary classification case
            confidence = float(prediction)  # scalar
            pred_label = self.class_labels[1] if confidence >= 0.5 else self.class_labels[0]
            return {
                "prediction": pred_label,
                "confidence": confidence if confidence >= 0.5 else 1 - confidence,
                "probabilities": {
                    self.class_labels[0]: 1 - confidence,
                    self.class_labels[1]: confidence
                }
            }
        # else:
        #     print("Multi-class")
        #     # Multi-class case
        #     pred_index = np.argmax(prediction)
        #     pred_label = self.class_labels[pred_index]
        #     confidence = prediction[pred_index]
        #     return {
        #         "prediction": pred_label,
        #         "confidence": float(confidence),
        #         "probabilities": {
        #             self.class_labels[i]: float(prediction[i]) for i in range(len(self.class_labels))
        #         }
        #     }
