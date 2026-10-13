"""Dataset management and labeling package for Smart Jasmine Farming Assistant."""

from src.dataset.duplicate_detector import compute_exact_hash, compute_dhash, find_duplicates
from src.dataset.organizer import (
    scan_raw_dataset,
    prepare_dataset_splits,
    get_dataset_summary,
    PHOTOGRAPHY_GUIDELINES,
)
from src.dataset.labeling import label_single_bud_image, stage_whole_plant_image

__all__ = [
    "compute_exact_hash",
    "compute_dhash",
    "find_duplicates",
    "scan_raw_dataset",
    "prepare_dataset_splits",
    "get_dataset_summary",
    "PHOTOGRAPHY_GUIDELINES",
    "label_single_bud_image",
    "stage_whole_plant_image",
]
