"""
Dataset Organizer, Splitting, and Quality Auditor for Smart Jasmine Farming Assistant.
Maintains strict separation between labeled buds, unlabeled photos, and whole-plant images.
"""

import os
import json
import random
import shutil
from pathlib import Path
from typing import Dict, List, Any, Tuple
from PIL import Image

from config.settings import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    FLOWER_STAGES,
)
from src.dataset.duplicate_detector import compute_exact_hash, compute_dhash, hamming_distance

# Specific Subdirectories
SINGLE_BUDS_RAW = RAW_DATA_DIR / "single_buds"
WHOLE_PLANT_RAW = RAW_DATA_DIR / "whole_plant"

PROCESSED_TRAIN = PROCESSED_DATA_DIR / "train"
PROCESSED_VAL = PROCESSED_DATA_DIR / "val"
PROCESSED_TEST = PROCESSED_DATA_DIR / "test"

MANIFEST_PATH = PROCESSED_DATA_DIR / "dataset_manifest.json"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# Minimum threshold for a robust training dataset per class
RECOMMENDED_MIN_PER_CLASS = 150
STARTER_THRESHOLD_PER_CLASS = 40

# Practical Photography Protocol for the Grower & Family
PHOTOGRAPHY_GUIDELINES = [
    {
        "title": "Natural Morning Daylight (காலை இயற்கை வெளிச்சம்)",
        "guideline": "Photograph buds between 6:30 AM and 8:30 AM. Avoid harsh midday direct sunlight which washes out white petals and creates sharp black shadows.",
    },
    {
        "title": "Macro Distance & Focus (சரியான தூரம் & கூர்மை)",
        "guideline": "Keep camera 10 to 20 cm from the bud. Tap the smartphone screen directly on the bud tip to lock focus before snapping. Ensure the background is slightly blurred.",
    },
    {
        "title": "Angle Variety (பல்வேறு கோணங்கள்)",
        "guideline": "Capture at least 3 distinct angles for each bud: (1) Side profile showing bud elongation and corolla tube, (2) Top-down view showing petal tightness, (3) Calyx base showing sepals and stalk.",
    },
    {
        "title": "Background Diversity (பின்னணி வேறுபாடு)",
        "guideline": "Photograph buds against diverse natural backgrounds: dark green mature foliage, lighter tender leaves, farmer's fingers holding the stem, and ground soil.",
    },
    {
        "title": "Documenting Damaged Buds (சேதமடைந்த மொட்டுகள்)",
        "guideline": "Specifically seek and photograph buds attacked by Bud Worm (silk webbing, boreholes, reddish-brown feces) and Blossom Midge (pale brown discoloration and base rotting).",
    },
    {
        "title": "Keep Whole-Plant Photos Separate (முழு செடி புகைப்படங்களை தனித்து வையுங்கள்)",
        "guideline": "Do not mix wide whole-plant bush photos with single bud photos. Whole-plant photos contain dozens of overlapping buds and require bounding-box annotation in Phase 7.",
    },
]


def scan_raw_dataset() -> Dict[str, Any]:
    """
    Scans data/raw/ directory and categorizes images by stage and type.
    Ensures complete isolation between labeled single buds and whole-plant photos.
    """
    stage_counts: Dict[str, int] = {stage: 0 for stage in FLOWER_STAGES}
    stage_files: Dict[str, List[Path]] = {stage: [] for stage in FLOWER_STAGES}

    unlabeled_files: List[Path] = []
    whole_plant_files: List[Path] = []

    # 1. Scan single buds by class
    for stage in FLOWER_STAGES:
        stage_dir = SINGLE_BUDS_RAW / stage
        if stage_dir.is_dir():
            for p in stage_dir.iterdir():
                if p.suffix.lower() in IMAGE_EXTENSIONS:
                    stage_counts[stage] += 1
                    stage_files[stage].append(p)

    # Also check legacy root data/raw for backward compatibility
    if RAW_DATA_DIR.is_dir():
        for p in RAW_DATA_DIR.iterdir():
            if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS:
                # Check if file name contains stage
                matched = False
                for stage in FLOWER_STAGES:
                    if stage.lower() in p.name.lower():
                        stage_counts[stage] += 1
                        stage_files[stage].append(p)
                        matched = True
                        break
                if not matched:
                    unlabeled_files.append(p)

    # 2. Scan single buds / unlabeled
    unlabeled_dir = SINGLE_BUDS_RAW / "unlabeled"
    if unlabeled_dir.is_dir():
        for p in unlabeled_dir.iterdir():
            if p.suffix.lower() in IMAGE_EXTENSIONS:
                unlabeled_files.append(p)

    # 3. Scan whole-plant directory
    whole_plant_dir = WHOLE_PLANT_RAW / "incoming"
    if whole_plant_dir.is_dir():
        for p in whole_plant_dir.iterdir():
            if p.suffix.lower() in IMAGE_EXTENSIONS:
                whole_plant_files.append(p)

    total_labeled_single = sum(stage_counts.values())

    return {
        "stage_counts": stage_counts,
        "stage_files": stage_files,
        "total_labeled_single_buds": total_labeled_single,
        "unlabeled_single_buds_count": len(unlabeled_files),
        "unlabeled_files": [str(p) for p in unlabeled_files],
        "whole_plant_count": len(whole_plant_files),
        "whole_plant_files": [str(p) for p in whole_plant_files],
    }


def get_dataset_summary() -> Dict[str, Any]:
    """
    Returns an honest, critical dataset readiness assessment.
    Warns that a small dataset cannot produce a reliable model.
    """
    scan = scan_raw_dataset()
    stage_counts = scan["stage_counts"]
    total = scan["total_labeled_single_buds"]

    # Readiness Assessment
    min_count = min(stage_counts.values()) if stage_counts else 0
    max_count = max(stage_counts.values()) if stage_counts else 0
    imbalance_ratio = round(max_count / max(min_count, 1), 2)

    if total < len(FLOWER_STAGES) * 10:
        readiness_status = "INSUFFICIENT_FOR_TRAINING"
        readiness_message = (
            "⚠️ Current dataset is a small starter sample. It is strictly INSUFFICIENT for reliable deep learning. "
            "Model training must wait until at least 40-50 varied photographs per class are gathered."
        )
    elif min_count < STARTER_THRESHOLD_PER_CLASS:
        readiness_status = "MINIMAL_EXPERIMENTAL_ONLY"
        readiness_message = (
            "⚠️ Dataset contains enough photos for pipeline testing and code validation only. "
            f"One or more classes have fewer than {STARTER_THRESHOLD_PER_CLASS} photos. High risk of overfitting."
        )
    else:
        readiness_status = "TRAINING_READY"
        readiness_message = (
            "✓ Dataset has reached basic training threshold for transfer learning (MobileNetV2). "
            "Continuous data collection remains recommended."
        )

    return {
        "scan": scan,
        "total_labeled": total,
        "min_class_count": min_count,
        "max_class_count": max_count,
        "imbalance_ratio": imbalance_ratio,
        "readiness_status": readiness_status,
        "readiness_message": readiness_message,
        "recommended_min_per_class": RECOMMENDED_MIN_PER_CLASS,
        "guidelines": PHOTOGRAPHY_GUIDELINES,
    }


def prepare_dataset_splits(
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    near_dup_threshold: int = 4,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """
    Splits labeled single-bud images into train, val, and test partitions.
    Guarantees:
    1. Unlabeled images are NEVER included in training splits.
    2. Whole-plant photos are NEVER included in single-bud splits.
    3. Near-identical photos (dHash distance <= threshold) are placed in the SAME split
       to prevent data leakage between training and testing.
    4. Writes dataset_manifest.json with hashes and split allocations.
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-4, "Ratios must sum to 1.0"

    scan = scan_raw_dataset()
    stage_files = scan["stage_files"]

    # Clear destination processed directories
    for split_dir in [PROCESSED_TRAIN, PROCESSED_VAL, PROCESSED_TEST]:
        for stage in FLOWER_STAGES:
            target_dir = split_dir / stage
            target_dir.mkdir(parents=True, exist_ok=True)
            # Clean old files
            for old_f in target_dir.iterdir():
                if old_f.is_file():
                    old_f.unlink()

    manifest: List[Dict[str, Any]] = []
    split_summary: Dict[str, Dict[str, int]] = {
        "train": {s: 0 for s in FLOWER_STAGES},
        "val": {s: 0 for s in FLOWER_STAGES},
        "test": {s: 0 for s in FLOWER_STAGES},
    }

    random.seed(random_seed)

    for stage, paths in stage_files.items():
        if not paths:
            continue

        # Compute dHash for each image in this class to cluster near-duplicates
        clusters: List[List[Path]] = []
        cluster_hashes: List[int] = []

        for p in paths:
            try:
                with Image.open(p) as img:
                    h = compute_dhash(img)
            except Exception:
                continue

            # Check if this image belongs to an existing cluster (near-duplicate)
            assigned = False
            for c_idx, ch in enumerate(cluster_hashes):
                if hamming_distance(h, ch) <= near_dup_threshold:
                    clusters[c_idx].append(p)
                    assigned = True
                    break

            if not assigned:
                clusters.append([p])
                cluster_hashes.append(h)

        # Shuffle clusters
        random.shuffle(clusters)

        n_clusters = len(clusters)
        n_train = max(1, int(n_clusters * train_ratio)) if n_clusters >= 3 else n_clusters
        n_val = max(1, int(n_clusters * val_ratio)) if (n_clusters - n_train) >= 2 else (1 if n_clusters > 1 else 0)

        train_clusters = clusters[:n_train]
        val_clusters = clusters[n_train:n_train + n_val]
        test_clusters = clusters[n_train + n_val:]

        # Fallback if too few clusters
        if not test_clusters and len(val_clusters) > 1:
            test_clusters = [val_clusters.pop()]

        split_assignments = [
            ("train", train_clusters, PROCESSED_TRAIN),
            ("val", val_clusters, PROCESSED_VAL),
            ("test", test_clusters, PROCESSED_TEST),
        ]

        for split_name, cluster_list, target_root in split_assignments:
            for cluster in cluster_list:
                for img_path in cluster:
                    dest_path = target_root / stage / img_path.name
                    shutil.copy2(img_path, dest_path)
                    split_summary[split_name][stage] += 1

                    manifest.append({
                        "filename": img_path.name,
                        "source_path": str(img_path),
                        "dest_path": str(dest_path),
                        "stage": stage,
                        "split": split_name,
                        "sha256": compute_exact_hash(img_path),
                    })

    # Save manifest
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "manifest_version": "1.0",
            "total_samples": len(manifest),
            "split_summary": split_summary,
            "samples": manifest,
        }, f, indent=2)

    return {
        "status": "SUCCESS",
        "total_split_samples": len(manifest),
        "split_summary": split_summary,
        "manifest_path": str(MANIFEST_PATH),
    }
