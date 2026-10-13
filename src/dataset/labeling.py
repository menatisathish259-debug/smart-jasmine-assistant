"""
Labeling Workflow Utility for Smart Jasmine Farming Assistant.
Assigns ground-truth labels to single buds and stages whole-plant photographs.
"""

import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from PIL import Image

from config.settings import FLOWER_STAGES
from src.dataset.organizer import SINGLE_BUDS_RAW, WHOLE_PLANT_RAW
from src.database import repository
from src.core.validation import validate_image_file


def label_single_bud_image(
    source_path: Path,
    target_stage: str,
    notes: Optional[str] = None,
    section_id: Optional[int] = None,
    db_path: Optional[Path] = None,
) -> Dict[str, Any]:

    """
    Labels an incoming or unlabeled single-bud photograph.
    Moves it to data/raw/single_buds/<target_stage>/ and records it in SQLite image_labels.
    """
    if target_stage not in FLOWER_STAGES:
        raise ValueError(f"Invalid stage '{target_stage}'. Must be one of {FLOWER_STAGES}")

    target_dir = SINGLE_BUDS_RAW / target_stage
    target_dir.mkdir(parents=True, exist_ok=True)

    dest_path = target_dir / source_path.name
    # Avoid collision by appending timestamp if exists
    if dest_path.exists() and dest_path != source_path:
        stem = source_path.stem
        suffix = source_path.suffix
        dest_path = target_dir / f"{stem}_labeled{suffix}"

    if source_path != dest_path:
        shutil.move(str(source_path), str(dest_path))

    # Read image metadata
    width, height, img_format, size_kb = None, None, None, None
    try:
        with Image.open(dest_path) as img:
            width, height = img.size
            img_format = img.format
            size_kb = round(dest_path.stat().st_size / 1024, 1)
    except Exception:
        pass

    # Save to SQLite image_labels table
    db_id = repository.add_image_label(
        filename=dest_path.name,
        filepath=str(dest_path),
        label_stage=target_stage,
        image_type="single_bud",
        section_id=section_id,
        labeled_by="grower",
        width=width,
        height=height,
        format=img_format,
        filesize_kb=size_kb,
        notes=notes,
        db_path=db_path,
    )

    return {
        "status": "SUCCESS",
        "new_path": str(dest_path),
        "stage": target_stage,
        "label_id": db_id,
    }


def stage_whole_plant_image(
    source_path: Path,
    notes: Optional[str] = None,
    section_id: Optional[int] = None,
    db_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Stages a whole-plant bush photograph into data/raw/whole_plant/incoming/.
    Strictly segregated from single-bud training data until Phase 7 bounding box labeling.
    """
    target_dir = WHOLE_PLANT_RAW / "incoming"
    target_dir.mkdir(parents=True, exist_ok=True)

    dest_path = target_dir / source_path.name
    if source_path != dest_path:
        shutil.copy2(str(source_path), str(dest_path))

    width, height, img_format, size_kb = None, None, None, None
    try:
        with Image.open(dest_path) as img:
            width, height = img.size
            img_format = img.format
            size_kb = round(dest_path.stat().st_size / 1024, 1)
    except Exception:
        pass

    db_id = repository.add_image_label(
        filename=dest_path.name,
        filepath=str(dest_path),
        label_stage="NOT_READY",  # default placeholder constraint
        image_type="whole_plant",
        section_id=section_id,
        labeled_by="grower",
        width=width,
        height=height,
        format=img_format,
        filesize_kb=size_kb,
        notes=f"Whole-plant staging for YOLO Phase 7. {notes or ''}".strip(),
        db_path=db_path,
    )


    return {
        "status": "SUCCESS",
        "new_path": str(dest_path),
        "image_type": "whole_plant",
        "label_id": db_id,
    }
