"""
Model Training Pipeline for Jasminum sambac Flower Maturity Classification.
Trains MobileNetV2 with dataset sufficiency validation and experimental safety safeguards.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
import tensorflow as tf
from tensorflow import keras

from config.settings import (
    PROCESSED_DATA_DIR,
    MODELS_DIR,
    REPORTS_DIR,
    FLOWER_STAGES,
)
from src.dataset.organizer import get_dataset_summary, scan_raw_dataset
from src.models.classifier import build_mobilenetv2_classifier
from src.utils.logger import get_logger

logger = get_logger()

DEFAULT_MODEL_PATH = MODELS_DIR / "flower_stage_mobilenetv2.keras"
TRAINING_REPORT_PATH = REPORTS_DIR / "training_history.json"


def train_flower_classifier(
    train_dir: Optional[Path] = None,
    val_dir: Optional[Path] = None,
    epochs: int = 10,
    batch_size: int = 8,
    model_save_path: Optional[Path] = None,
    pretrained_weights: Optional[str] = "imagenet",
) -> Dict[str, Any]:
    """
    Executes MobileNetV2 transfer-learning training.
    Validates dataset sufficiency first and emits clear experimental disclaimers.
    """
    target_train = train_dir or (PROCESSED_DATA_DIR / "train")
    target_val = val_dir or (PROCESSED_DATA_DIR / "val")
    save_path = model_save_path or DEFAULT_MODEL_PATH

    save_path.parent.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Dataset Sufficiency Inspection
    summary = get_dataset_summary()
    total_samples = summary["total_labeled"]
    readiness_status = summary["readiness_status"]

    logger.info(f"Dataset Inspection: {total_samples} labeled single buds. Status: {readiness_status}")

    # Safety Guard: Refuse to train if classes have 0 samples
    stage_counts = summary["scan"]["stage_counts"]
    empty_classes = [s for s, count in stage_counts.items() if count == 0]
    if empty_classes and not (target_train / FLOWER_STAGES[0]).is_dir():
        msg = f"Cannot train: The following classes have 0 labeled photos: {', '.join(empty_classes)}. Please label at least a few photos per stage."
        logger.warning(msg)
        return {
            "status": "ABORTED_INSUFFICIENT_DATA",
            "message": msg,
            "readiness_status": readiness_status,
            "empty_classes": empty_classes,
        }

    is_experimental = (readiness_status != "TRAINING_READY")
    experimental_warning = (
        "⚠️ EXPERIMENTAL PIPELINE EXECUTION: Dataset is small (< 150/class). "
        "The trained model is for software verification and learning only. "
        "NEVER make commercial harvest commitments based solely on these predictions."
    ) if is_experimental else "Production-scale dataset verified."

    # 2. Build tf.data datasets
    try:
        train_ds = keras.utils.image_dataset_from_directory(
            str(target_train),
            labels="inferred",
            label_mode="int",
            class_names=FLOWER_STAGES,
            batch_size=batch_size,
            image_size=(224, 224),
            shuffle=True,
            seed=42,
        )

        val_ds = keras.utils.image_dataset_from_directory(
            str(target_val),
            labels="inferred",
            label_mode="int",
            class_names=FLOWER_STAGES,
            batch_size=batch_size,
            image_size=(224, 224),
            shuffle=False,
            seed=42,
        )
    except Exception as e:
        msg = f"Failed to load dataset from processed directories: {e}. Please run dataset partitioning first."
        logger.error(msg)
        return {
            "status": "ERROR_LOADING_DATASET",
            "message": msg,
        }

    # Performance optimizations for tf.data
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

    # 3. Model Construction
    logger.info("Instantiating MobileNetV2 architecture with ImageNet feature base...")
    model = build_mobilenetv2_classifier(
        num_classes=len(FLOWER_STAGES),
        input_shape=(224, 224, 3),
        learning_rate=1e-4,
        pretrained_weights=pretrained_weights,
    )

    # 4. Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
            verbose=1,
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            verbose=1,
        ),
        keras.callbacks.ModelCheckpoint(
            filepath=str(save_path),
            monitor="val_loss",
            save_best_only=True,
            verbose=1,
        ),
    ]

    # 5. Model Training Execution
    logger.info(f"Starting model fit for {epochs} epochs...")
    start_time = time.time()
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks,
        verbose=1,
    )
    elapsed_seconds = round(time.time() - start_time, 2)

    # Final save in Keras format
    model.save(str(save_path))
    logger.info(f"Model successfully saved to: {save_path}")

    # Extract history metrics
    final_metrics = {
        "train_loss": [float(v) for v in history.history.get("loss", [])],
        "train_accuracy": [float(v) for v in history.history.get("accuracy", [])],
        "val_loss": [float(v) for v in history.history.get("val_loss", [])],
        "val_accuracy": [float(v) for v in history.history.get("val_accuracy", [])],
    }

    report = {
        "status": "COMPLETED",
        "model_path": str(save_path),
        "epochs_trained": len(final_metrics["train_loss"]),
        "elapsed_seconds": elapsed_seconds,
        "is_experimental": is_experimental,
        "experimental_warning": experimental_warning,
        "final_train_accuracy": round(final_metrics["train_accuracy"][-1], 4) if final_metrics["train_accuracy"] else 0.0,
        "final_val_accuracy": round(final_metrics["val_accuracy"][-1], 4) if final_metrics["val_accuracy"] else 0.0,
        "history": final_metrics,
    }

    # Save training report JSON
    with open(TRAINING_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return report
