"""
Model Evaluation and Error Analysis for Jasminum sambac Classifier.
Calculates independent test set metrics, confusion matrix, precision, recall, and critical failure cases.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import classification_report, confusion_matrix

from config.settings import (
    PROCESSED_DATA_DIR,
    MODELS_DIR,
    REPORTS_DIR,
    FLOWER_STAGES,
)
from src.utils.logger import get_logger

logger = get_logger()

EVALUATION_REPORT_PATH = REPORTS_DIR / "evaluation_metrics.json"


def evaluate_model(
    model_path: Optional[Path] = None,
    test_dir: Optional[Path] = None,
    batch_size: int = 8,
) -> Dict[str, Any]:
    """
    Evaluates the saved model on the test partition.
    Produces confusion matrix, per-class metrics, and critical commercial failure analysis.
    """
    target_model_path = model_path or (MODELS_DIR / "flower_stage_mobilenetv2.keras")
    target_test_dir = test_dir or (PROCESSED_DATA_DIR / "test")

    if not target_model_path.exists():
        msg = f"Model checkpoint not found at: {target_model_path}. Train the model first."
        logger.error(msg)
        return {"status": "MODEL_NOT_FOUND", "message": msg}

    if not target_test_dir.exists():
        msg = f"Test directory not found at: {target_test_dir}. Prepare dataset splits first."
        logger.error(msg)
        return {"status": "TEST_DATA_NOT_FOUND", "message": msg}

    logger.info(f"Loading model checkpoint from {target_model_path} for independent evaluation...")
    model = keras.models.load_model(str(target_model_path))

    # Load test dataset
    try:
        test_ds = keras.utils.image_dataset_from_directory(
            str(target_test_dir),
            labels="inferred",
            label_mode="int",
            class_names=FLOWER_STAGES,
            batch_size=batch_size,
            image_size=(224, 224),
            shuffle=False,
        )
    except Exception as e:
        msg = f"Error loading test images: {e}"
        logger.error(msg)
        return {"status": "ERROR_LOADING_TEST_DATA", "message": msg}

    # Extract all true labels and predicted probabilities
    y_true = []
    y_pred_probs = []

    for images, labels in test_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(labels.numpy())
        y_pred_probs.extend(preds)

    if not y_true:
        return {"status": "EMPTY_TEST_SET", "message": "Test set contains 0 images."}

    y_true = np.array(y_true)
    y_pred_probs = np.array(y_pred_probs)
    y_pred = np.argmax(y_pred_probs, axis=1)

    # Calculate overall accuracy
    overall_accuracy = float(np.mean(y_true == y_pred))

    # Confusion matrix
    conf_mat = confusion_matrix(y_true, y_pred, labels=list(range(len(FLOWER_STAGES))))

    # Per-class classification report
    report_dict = classification_report(
        y_true,
        y_pred,
        target_names=FLOWER_STAGES,
        output_dict=True,
        zero_division=0,
    )

    # Critical Commercial Risk Analysis
    # Risk 1: Picking NOT_READY buds as READY_TO_PLUCK (leads to weight loss & bad opening)
    idx_ready = FLOWER_STAGES.index("READY_TO_PLUCK")
    idx_not_ready = FLOWER_STAGES.index("NOT_READY")
    idx_damaged = FLOWER_STAGES.index("DAMAGED_OR_ABNORMAL")

    premature_pick_errors = int(conf_mat[idx_not_ready, idx_ready])
    # Risk 2: Packing DAMAGED buds into commercial ready harvest (causes market penalty)
    damaged_packed_errors = int(conf_mat[idx_damaged, idx_ready])

    per_class_summary = {}
    for stage in FLOWER_STAGES:
        stage_metrics = report_dict.get(stage, {})
        per_class_summary[stage] = {
            "precision": round(stage_metrics.get("precision", 0.0), 3),
            "recall": round(stage_metrics.get("recall", 0.0), 3),
            "f1_score": round(stage_metrics.get("f1-score", 0.0), 3),
            "support": int(stage_metrics.get("support", 0)),
        }

    evaluation_report = {
        "status": "COMPLETED",
        "total_test_samples": len(y_true),
        "overall_test_accuracy": round(overall_accuracy, 4),
        "per_class_metrics": per_class_summary,
        "confusion_matrix": conf_mat.tolist(),
        "stages": FLOWER_STAGES,
        "critical_commercial_risks": {
            "premature_plucking_false_positives": premature_pick_errors,
            "damaged_bud_false_positives": damaged_packed_errors,
            "interpretation": (
                f"{premature_pick_errors} immature buds were falsely predicted as ready; "
                f"{damaged_packed_errors} damaged buds were falsely predicted as ready."
            ),
        },
        "disclaimer": (
            "⚠️ INDEPENDENT EVALUATION RESULT: Evaluated strictly on the held-out test split. "
            "Never extrapolate laboratory accuracy to outdoor field performance without verified grower oversight."
        ),
    }

    # Save to reports
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(EVALUATION_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(evaluation_report, f, indent=2)

    logger.info(f"Evaluation report successfully saved to: {EVALUATION_REPORT_PATH}")
    return evaluation_report
