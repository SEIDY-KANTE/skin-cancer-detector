import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

def plot_training_curves(history):
    """Visualize accuracy and loss curves."""
    plt.figure(figsize=(14, 5))

    # Accuracy
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train')
    plt.plot(history.history['val_accuracy'], label='Validation')
    plt.title('Accuracy over Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    # Loss
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train')
    plt.plot(history.history['val_loss'], label='Validation')
    plt.title('Loss over Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.tight_layout()
    plt.show()

def evaluate_model(model, test_generator, class_labels=["Cancer", "Non_Cancer"]):
    """Evaluate model performance on the test set."""
    print("[INFO] Evaluating model on test set...")
    Y_pred = model.predict(test_generator)
    y_pred = (Y_pred > 0.5).astype(int).ravel()

    true_labels = test_generator.classes
    target_names = class_labels

    print("\nClassification Report:")
    print(classification_report(true_labels, y_pred, target_names=target_names))

    cm = confusion_matrix(true_labels, y_pred)

    # Plot confusion matrix
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=target_names, yticklabels=target_names)
    plt.title("Confusion Matrix")
    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    plt.show()
