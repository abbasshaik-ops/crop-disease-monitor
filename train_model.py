# train_model.py
import os
import json
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models

# Configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
TRAIN_DIR = "dataset/train"
VAL_DIR = "dataset/val"
MODEL_SAVE_PATH = "models/crop_disease_model.keras"
LABELS_SAVE_PATH = "models/class_labels.json"

def train():
    if not os.path.exists(TRAIN_DIR) or not os.listdir(TRAIN_DIR):
        raise FileNotFoundError(f"Please add class folders with images inside '{TRAIN_DIR}' first.")

    # 1. Load Datasets
    train_ds = tf.keras.utils.image_dataset_from_directory(
        TRAIN_DIR,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical"
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        VAL_DIR,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical"
    )

    class_names = train_ds.class_names
    num_classes = len(class_names)
    print(f"Detected Classes ({num_classes}): {class_names}")

    # Save class names for inference later
    os.makedirs("models", exist_ok=True)
    with open(LABELS_SAVE_PATH, "w") as f:
        json.dump(class_names, f)

    # Optimize performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

    # 2. Data Augmentation & Preprocessing
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.15),
    ])

    preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input

    # 3. Build Transfer Learning Model (MobileNetV2)
    base_model = MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False  # Freeze base weights for fast CPU training

    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = data_augmentation(inputs)
    x = preprocess_input(x)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = models.Model(inputs, outputs)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    # 4. Train
    print("Starting training...")
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS
    )

    # 5. Save Model
    model.save(MODEL_SAVE_PATH)
    print(f"Model saved successfully to {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    train()