"""
Unit tests for Phase 5: MobileNetV2 architecture, training pipeline, evaluation, and inference.
"""

from pathlib import Path
from PIL import Image
import numpy as np
import pytest

from config.settings import FLOWER_STAGES
from src.models.classifier import (
    build_mobilenetv2_classifier,
    unfreeze_for_fine_tuning,
)
from src.models.training import train_flower_classifier
from src.models.evaluator import evaluate_model
from src.models.inference import predict_flower_stage, is_model_available


def create_synthetic_image(path: Path, color=(255, 255, 255), size=(224, 224)):
    """Creates a sample test image for testing."""
    img = Image.new("RGB", size, color=color)
    img.save(path, format="JPEG")


def test_build_mobilenetv2_classifier_structure():
    """Verify MobileNetV2 transfer-learning model architecture and frozen base."""
    # Use pretrained_weights=None for rapid offline unit test
    model = build_mobilenetv2_classifier(
        num_classes=4,
        input_shape=(224, 224, 3),
        pretrained_weights=None,
    )

    assert model.input_shape == (None, 224, 224, 3)
    assert model.output_shape == (None, 4)

    # Check that base MobileNetV2 is frozen
    base_model = None
    for layer in model.layers:
        if "mobilenetv2" in layer.name.lower():
            base_model = layer
            break

    assert base_model is not None, "Base MobileNetV2 layer must be present"
    assert base_model.trainable is False, "Base model must be frozen for transfer learning"


def test_unfreeze_for_fine_tuning():
    """Verify top layer unfreezing for fine tuning."""
    model = build_mobilenetv2_classifier(num_classes=4, pretrained_weights=None)
    model = unfreeze_for_fine_tuning(model, num_layers_to_unfreeze=15)

    base_model = [l for l in model.layers if "mobilenetv2" in l.name.lower()][0]
    assert base_model.trainable is True


def test_training_aborts_on_empty_dataset(tmp_path):
    """Verify that training pipeline refuses to execute on empty classes and outputs honest warning."""
    empty_train_dir = tmp_path / "train"
    empty_val_dir = tmp_path / "val"
    for s in FLOWER_STAGES:
        (empty_train_dir / s).mkdir(parents=True)
        (empty_val_dir / s).mkdir(parents=True)

    result = train_flower_classifier(
        train_dir=empty_train_dir,
        val_dir=empty_val_dir,
        epochs=1,
    )

    assert result["status"] in ("ABORTED_INSUFFICIENT_DATA", "ERROR_LOADING_DATASET")


def test_evaluator_missing_model(tmp_path):
    """Verify evaluator handles missing checkpoint safely."""
    fake_path = tmp_path / "non_existent_model.keras"
    res = evaluate_model(model_path=fake_path)
    assert res["status"] == "MODEL_NOT_FOUND"


def test_inference_pipeline_with_mock_checkpoint(tmp_path):
    """Verify inference pipeline produces full distributions, uncertainty, and disclaimers."""
    test_model_path = tmp_path / "test_model.keras"
    model = build_mobilenetv2_classifier(num_classes=4, pretrained_weights=None)
    model.save(str(test_model_path))

    # Test image
    img = Image.new("RGB", (224, 224), color=(250, 245, 240))
    res = predict_flower_stage(img, model_path=test_model_path)

    assert res["status"] == "SUCCESS"
    assert res["predicted_stage"] in FLOWER_STAGES
    assert 0.0 <= res["confidence_pct"] <= 100.0
    assert 0.0 <= res["uncertainty_score"] <= 1.0
    assert len(res["probabilities"]) == 4
    assert sum(res["probabilities"].values()) == pytest.approx(100.0, abs=0.5)
    assert "EXPERIMENTAL AI PREDICTION" in res["disclaimer"]
    assert "status_title" in res["guidance"]
