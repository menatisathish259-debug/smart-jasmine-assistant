"""
MobileNetV2 Transfer Learning Architecture for Jasminum sambac Flower Maturity Classification.
Includes sunlight/angle data augmentation and regularized classification head.
"""

from typing import Tuple, Optional
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from config.settings import FLOWER_STAGES


def build_data_augmentation() -> keras.Sequential:
    """Builds robust data augmentation layers for field conditions (sunlight, angles, wind)."""
    return keras.Sequential(
        [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.15),  # Handles flower orientation variations
            layers.RandomZoom(0.1),       # Handles camera distance variations
            layers.RandomContrast(0.15),  # Handles bright sun vs cloud variations
        ],
        name="data_augmentation",
    )


def build_mobilenetv2_classifier(
    num_classes: int = len(FLOWER_STAGES),
    input_shape: Tuple[int, int, int] = (224, 224, 3),
    dropout_rate: float = 0.35,
    learning_rate: float = 1e-4,
    pretrained_weights: Optional[str] = "imagenet",
) -> keras.Model:
    """
    Constructs a MobileNetV2 transfer-learning model tailored for jasmine bud classification.
    Base layers are initially frozen for stable transfer learning on small datasets.
    """
    # 1. Input layer
    inputs = layers.Input(shape=input_shape, name="input_image")

    # 2. Data augmentation (active during training only)
    augmentation = build_data_augmentation()
    x = augmentation(inputs)

    # 3. MobileNetV2 Preprocessing (-1 to +1 normalization)
    x = keras.applications.mobilenet_v2.preprocess_input(x)

    # 4. MobileNetV2 Base Feature Extractor
    base_model = keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights=pretrained_weights,
    )
    base_model.trainable = False  # Freeze base weights for Phase 1 transfer learning

    x = base_model(x, training=False)

    # 5. Classification Head
    x = layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
    x = layers.BatchNormalization(name="batch_norm")(x)
    x = layers.Dense(
        128,
        activation="relu",
        kernel_regularizer=keras.regularizers.l2(1e-4),
        name="dense_feature_projection",
    )(x)
    x = layers.Dropout(dropout_rate, name="dropout_regularization")(x)

    outputs = layers.Dense(
        num_classes,
        activation="softmax",
        name="flower_stage_probabilities",
    )(x)

    model = keras.Model(inputs=inputs, outputs=outputs, name="JasmineFlowerMobileNetV2")

    # 6. Compile
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


def unfreeze_for_fine_tuning(
    model: keras.Model,
    num_layers_to_unfreeze: int = 30,
    fine_tune_lr: float = 1e-5,
) -> keras.Model:
    """
    Unfreezes top convolutional layers of MobileNetV2 for gentle fine-tuning
    at a lower learning rate. Recommended only when dataset reaches >100 images per class.
    """
    base_model = None
    for layer in model.layers:
        if "mobilenetv2" in layer.name.lower():
            base_model = layer
            break

    if base_model is None:
        raise ValueError("MobileNetV2 base model layer not found in model.")

    base_model.trainable = True
    # Freeze all except top N layers
    for layer in base_model.layers[:-num_layers_to_unfreeze]:
        layer.trainable = False

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=fine_tune_lr),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model
