import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization, Input
from keras._tf_keras.keras.preprocessing.image import ImageDataGenerator
from callbacks import get_callbacks
from evaluate import evaluate_model, plot_training_curves
import json

class SkinCancerClassifier:
    def __init__(self, train_dir, test_dir, img_size=(224, 224), batch_size=32):
        self.train_dir = train_dir
        self.test_dir = test_dir
        self.img_size = img_size
        self.batch_size = batch_size
        self.model = None

    def load_data(self):
        """Load training and testing datasets with augmentation."""
        datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            zoom_range=0.2,
            shear_range=0.2,
            horizontal_flip=True
        )

        self.train_data = datagen.flow_from_directory(
            self.train_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='binary'
        )

        self.test_data = ImageDataGenerator(rescale=1./255).flow_from_directory(
            self.test_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='binary',
            shuffle=False 
        )

    def build_model(self):
        """Build CNN model architecture."""
        self.model = Sequential([
            Input(shape=(*self.img_size, 3)),
            Conv2D(32, (3, 3), activation='relu'),
            BatchNormalization(),
            MaxPooling2D(2, 2),

            Conv2D(64, (3, 3), activation='relu'),
            BatchNormalization(),
            MaxPooling2D(2, 2),

            Conv2D(128, (3, 3), activation='relu'),
            BatchNormalization(),
            MaxPooling2D(2, 2),

            Flatten(),
            Dense(256, activation='relu'),
            Dropout(0.5),
            Dense(1, activation='sigmoid')
        ])

        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

    def train(self, epochs=30):
        """Train the CNN model and evaluate it."""
        self.load_data()
        self.build_model()
        callbacks = get_callbacks()

        history = self.model.fit(
            self.train_data,
            validation_data=self.test_data,
            epochs=epochs,
            callbacks=callbacks
        )

        self.model.save('skin_cancer_model.keras')

        plot_training_curves(history)
        evaluate_model(self.model, self.test_data)

        # Save training history
        with open('training_history.json', 'w') as f:
            json.dump(history.history, f)

if __name__ == "__main__":
    train_path = "../../dataset/processed_dataset/train"
    test_path = "../../dataset/processed_dataset/test"

    trainer = SkinCancerClassifier(train_path, test_path)
    trainer.train()

    # Plot training curves
    # with open('training_history.json', 'r') as f:
    #     history = json.load(f)
    
    # plot_training_curves(history)

    print("✅ Model training complete.")