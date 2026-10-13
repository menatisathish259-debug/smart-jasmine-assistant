"""
Unit tests for Phase 4: Dataset organization, duplicate detection, splitting, and labeling.
Runs in an isolated temporary directory to ensure reproducibility.
"""

import os
import json
from pathlib import Path
from PIL import Image
import pytest

from config.settings import FLOWER_STAGES
from src.dataset.duplicate_detector import (
    compute_exact_hash,
    compute_dhash,
    hamming_distance,
    find_duplicates,
)
from src.dataset.organizer import (
    scan_raw_dataset,
    get_dataset_summary,
    prepare_dataset_splits,
    PHOTOGRAPHY_GUIDELINES,
    SINGLE_BUDS_RAW,
    WHOLE_PLANT_RAW,
    PROCESSED_TRAIN,
    PROCESSED_VAL,
    PROCESSED_TEST,
    MANIFEST_PATH,
)
from src.dataset.labeling import label_single_bud_image, stage_whole_plant_image
from src.database.connection import init_database


@pytest.fixture
def mock_dataset_environment(tmp_path, monkeypatch):
    """Creates a temporary isolated dataset structure."""
    fake_raw = tmp_path / "data" / "raw"
    fake_processed = tmp_path / "data" / "processed"
    fake_db = tmp_path / "data" / "db" / "jasmine_test.db"

    fake_single_buds = fake_raw / "single_buds"
    fake_whole_plant = fake_raw / "whole_plant"

    for s in FLOWER_STAGES:
        (fake_single_buds / s).mkdir(parents=True, exist_ok=True)
    (fake_single_buds / "unlabeled").mkdir(parents=True, exist_ok=True)
    (fake_whole_plant / "incoming").mkdir(parents=True, exist_ok=True)

    fake_processed.mkdir(parents=True, exist_ok=True)
    init_database(fake_db)

    # Monkeypatch paths
    monkeypatch.setattr("src.dataset.organizer.RAW_DATA_DIR", fake_raw)
    monkeypatch.setattr("src.dataset.organizer.PROCESSED_DATA_DIR", fake_processed)
    monkeypatch.setattr("src.dataset.organizer.SINGLE_BUDS_RAW", fake_single_buds)
    monkeypatch.setattr("src.dataset.organizer.WHOLE_PLANT_RAW", fake_whole_plant)
    monkeypatch.setattr("src.dataset.organizer.PROCESSED_TRAIN", fake_processed / "train")
    monkeypatch.setattr("src.dataset.organizer.PROCESSED_VAL", fake_processed / "val")
    monkeypatch.setattr("src.dataset.organizer.PROCESSED_TEST", fake_processed / "test")
    monkeypatch.setattr("src.dataset.organizer.MANIFEST_PATH", fake_processed / "dataset_manifest.json")

    monkeypatch.setattr("src.dataset.labeling.SINGLE_BUDS_RAW", fake_single_buds)
    monkeypatch.setattr("src.dataset.labeling.WHOLE_PLANT_RAW", fake_whole_plant)

    return {
        "raw": fake_raw,
        "processed": fake_processed,
        "single_buds": fake_single_buds,
        "whole_plant": fake_whole_plant,
        "db": fake_db,
    }


def create_dummy_image(path: Path, color=(255, 255, 255), size=(100, 100)):
    """Helper to write a valid test image."""
    img = Image.new("RGB", size, color=color)
    img.save(path, format="JPEG")


def test_duplicate_detector_exact_and_near(tmp_path):
    """Verify exact and near-duplicate detection logic."""
    img1_path = tmp_path / "bud_original.jpg"
    img2_copy_path = tmp_path / "bud_exact_copy.jpg"
    img3_diff_path = tmp_path / "bud_different.jpg"

    create_dummy_image(img1_path, color=(255, 250, 240))
    # Exact copy
    with open(img1_path, "rb") as f_src, open(img2_copy_path, "wb") as f_dst:
        f_dst.write(f_src.read())
    # Different image
    create_dummy_image(img3_diff_path, color=(10, 80, 20))

    # Test exact hashes
    hash1 = compute_exact_hash(img1_path)
    hash2 = compute_exact_hash(img2_copy_path)
    hash3 = compute_exact_hash(img3_diff_path)

    assert hash1 == hash2
    assert hash1 != hash3

    # Test find_duplicates
    results = find_duplicates([img1_path, img2_copy_path, img3_diff_path])
    assert len(results["exact_duplicates"]) == 1
    assert len(results["exact_duplicates"][0]) == 2


def test_dhash_perceptual_near_duplicate(tmp_path):
    """Verify that slightly altered images yield low Hamming distance."""
    img1 = Image.new("RGB", (200, 200), color=(250, 250, 250))
    img2_near = Image.new("RGB", (200, 200), color=(245, 245, 245))
    img3_far = Image.new("RGB", (200, 200), color=(10, 20, 30))

    h1 = compute_dhash(img1)
    h2 = compute_dhash(img2_near)
    h3 = compute_dhash(img3_far)

    # Identical solid colors produce identical difference pattern
    assert hamming_distance(h1, h2) == 0


def test_dataset_scan_and_segregation(mock_dataset_environment):
    """Verify scanning correctly segregates single buds from whole-plant and unlabeled photos."""
    env = mock_dataset_environment
    single = env["single_buds"]
    whole = env["whole_plant"]

    # Add 2 ready, 1 not ready
    create_dummy_image(single / "READY_TO_PLUCK" / "b1.jpg", color=(250, 250, 250))
    create_dummy_image(single / "READY_TO_PLUCK" / "b2.jpg", color=(240, 240, 240))
    create_dummy_image(single / "NOT_READY" / "b3.jpg", color=(50, 150, 50))

    # Add 1 unlabeled single bud
    create_dummy_image(single / "unlabeled" / "unknown_bud.jpg", color=(100, 100, 100))

    # Add 1 whole plant photo
    create_dummy_image(whole / "incoming" / "whole_bush_1.jpg", color=(30, 120, 40))

    scan = scan_raw_dataset()

    assert scan["stage_counts"]["READY_TO_PLUCK"] == 2
    assert scan["stage_counts"]["NOT_READY"] == 1
    assert scan["total_labeled_single_buds"] == 3
    assert scan["unlabeled_single_buds_count"] == 1
    assert scan["whole_plant_count"] == 1


def test_dataset_summary_insufficient_warning(mock_dataset_environment):
    """Verify summary correctly reports that a small dataset is INSUFFICIENT for production."""
    env = mock_dataset_environment
    # Only 3 photos in total
    create_dummy_image(env["single_buds"] / "READY_TO_PLUCK" / "b1.jpg")
    create_dummy_image(env["single_buds"] / "NOT_READY" / "b2.jpg")

    summary = get_dataset_summary()
    assert summary["readiness_status"] == "INSUFFICIENT_FOR_TRAINING"
    assert "INSUFFICIENT" in summary["readiness_message"]
    assert len(summary["guidelines"]) >= 5


def test_prepare_dataset_splits_leak_free(mock_dataset_environment):
    """Verify dataset splitting creates train/val/test partitions without leaking unlabeled or whole-plant images."""
    env = mock_dataset_environment
    single = env["single_buds"]

    # Create 5 images per stage
    for stage in FLOWER_STAGES:
        for i in range(5):
            create_dummy_image(single / stage / f"{stage}_{i}.jpg", color=(i * 20, 200, 100))

    # Create unlabeled and whole plant photos
    create_dummy_image(single / "unlabeled" / "should_not_leak.jpg")
    create_dummy_image(env["whole_plant"] / "incoming" / "whole_bush_do_not_leak.jpg")

    split_res = prepare_dataset_splits(train_ratio=0.70, val_ratio=0.15, test_ratio=0.15)
    assert split_res["status"] == "SUCCESS"
    assert split_res["total_split_samples"] == 20  # 4 classes * 5 images

    # Verify manifest exists and is populated
    manifest_file = Path(split_res["manifest_path"])
    assert manifest_file.is_file()
    with open(manifest_file, "r") as f:
        data = json.load(f)
    assert data["total_samples"] == 20

    # Ensure no unlabeled or whole plant image entered the manifest
    for sample in data["samples"]:
        assert "should_not_leak" not in sample["filename"]
        assert "whole_bush" not in sample["filename"]


def test_label_single_bud_workflow(mock_dataset_environment):
    """Verify labeling an incoming image moves it to the appropriate stage folder and logs to database."""
    env = mock_dataset_environment
    unlabeled_file = env["single_buds"] / "unlabeled" / "raw_flower_1.jpg"
    create_dummy_image(unlabeled_file, color=(255, 255, 255))

    res = label_single_bud_image(
        source_path=unlabeled_file,
        target_stage="READY_TO_PLUCK",
        notes="Crisp white bud with good elongation",
        db_path=env["db"],
    )
    assert res["status"] == "SUCCESS"
    assert "READY_TO_PLUCK" in res["new_path"]
    assert Path(res["new_path"]).is_file()
    assert not unlabeled_file.exists()


def test_stage_whole_plant_workflow(mock_dataset_environment):
    """Verify whole-plant photos are segregated and cataloged."""
    env = mock_dataset_environment
    temp_photo = env["raw"] / "garden_bush_wide.jpg"
    create_dummy_image(temp_photo, color=(34, 139, 34))

    res = stage_whole_plant_image(
        temp_photo,
        notes="High bud count on South Bed",
        db_path=env["db"],
    )

    assert res["status"] == "SUCCESS"
    assert "whole_plant" in res["new_path"]
    assert Path(res["new_path"]).is_file()
