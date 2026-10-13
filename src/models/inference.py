"""
Inference Engine for Flower Maturity Prediction.
Performs single-image inference with probability distributions, uncertainty estimation, and safety guidance.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras

from config.settings import MODELS_DIR, FLOWER_STAGES, TAMIL_STAGE_TRANSLATIONS, TELUGU_STAGE_TRANSLATIONS
from src.core.constants import HARVEST_GUIDANCE

_LOADED_MODEL: Optional[keras.Model] = None
_LOADED_MODEL_PATH: Optional[str] = None

DEFAULT_MODEL_PATH = MODELS_DIR / "flower_stage_mobilenetv2.keras"


def is_model_available(model_path: Optional[Path] = None) -> bool:
    """Checks whether a trained model file exists on disk."""
    p = model_path or DEFAULT_MODEL_PATH
    return p.is_file()


def get_cached_model(model_path: Optional[Path] = None) -> keras.Model:
    """Loads and caches the model to avoid re-loading on every Streamlit interaction."""
    global _LOADED_MODEL, _LOADED_MODEL_PATH
    target_path = str(model_path or DEFAULT_MODEL_PATH)

    if _LOADED_MODEL is not None and _LOADED_MODEL_PATH == target_path:
        return _LOADED_MODEL

    if not Path(target_path).exists():
        raise FileNotFoundError(f"Model file not found at: {target_path}")

    model = keras.models.load_model(target_path)
    _LOADED_MODEL = model
    _LOADED_MODEL_PATH = target_path
    return model


def predict_flower_stage(
    image: Image.Image,
    model_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Runs MobileNetV2 inference on a PIL image.
    Returns predicted flower maturity stage, confidence, full probability distribution,
    uncertainty, and actionable field guidance.
    """
    target_path = model_path or DEFAULT_MODEL_PATH
    if not is_model_available(target_path):
        return {
            "status": "MODEL_NOT_AVAILABLE",
            "message": "No trained model checkpoint found in models/. Please run training first.",
        }

    model = get_cached_model(target_path)

    # Preprocessing
    rgb_image = image.convert("RGB").resize((224, 224), Image.Resampling.LANCZOS)
    img_array = np.array(rgb_image, dtype=np.float32)
    img_batch = np.expand_dims(img_array, axis=0)

    # Note: Model includes preprocess_input layer or raw inputs
    # If using keras.applications, apply preprocess_input
    preprocessed_batch = keras.applications.mobilenet_v2.preprocess_input(img_batch)

    # Inference
    probabilities = model.predict(preprocessed_batch, verbose=0)[0]

    top_idx = int(np.argmax(probabilities))
    top_stage = FLOWER_STAGES[top_idx]
    confidence = float(probabilities[top_idx])
    uncertainty = round(1.0 - confidence, 4)

    # Build full distribution map
    distribution = {
        FLOWER_STAGES[i]: round(float(probabilities[i]) * 100.0, 2)
        for i in range(len(FLOWER_STAGES))
    }

    # Actionable harvest advice
    guidance = HARVEST_GUIDANCE.get(top_stage, {})

    return {
        "status": "SUCCESS",
        "predicted_stage": top_stage,
        "predicted_stage_ta": TAMIL_STAGE_TRANSLATIONS.get(top_stage, top_stage),
        "predicted_stage_te": TELUGU_STAGE_TRANSLATIONS.get(top_stage, top_stage),
        "confidence_pct": round(confidence * 100.0, 2),
        "uncertainty_score": uncertainty,
        "probabilities": distribution,
        "guidance": guidance,
        "disclaimer": (
            "⚠️ EXPERIMENTAL AI PREDICTION: Model trained on small experimental dataset. "
            "Confidence reflects statistical image similarity, not guaranteed harvest readiness. "
            "The grower's field inspection is the ultimate ground truth."
        ),
    }
