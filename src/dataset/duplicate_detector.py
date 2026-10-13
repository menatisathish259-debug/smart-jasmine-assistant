"""
Duplicate and Near-Duplicate Image Detection for Smart Jasmine Dataset.
Prevents duplicate photographs from leaking between training, validation, and test splits.
"""

import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Set, Any
from PIL import Image


def compute_exact_hash(file_path: Path) -> str:
    """Computes SHA-256 cryptographic hash of image bytes for exact duplicate detection."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def compute_dhash(image: Image.Image, hash_size: int = 8) -> int:
    """
    Computes a 64-bit perceptual difference hash (dHash) using PIL.
    Fast, rotation/scale resilient, and detects burst or near-identical photographs.
    """
    # Resize to (hash_size + 1, hash_size) in grayscale
    resized = image.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    if hasattr(resized, "get_flattened_data"):
        pixels = list(resized.get_flattened_data())
    else:
        pixels = list(resized.getdata())


    diff_bits = 0
    for row in range(hash_size):
        row_offset = row * (hash_size + 1)
        for col in range(hash_size):
            left_pixel = pixels[row_offset + col]
            right_pixel = pixels[row_offset + col + 1]
            diff_bits = (diff_bits << 1) | (1 if left_pixel > right_pixel else 0)

    return diff_bits


def hamming_distance(hash1: int, hash2: int) -> int:
    """Calculates number of differing bits between two 64-bit hashes."""
    return bin(hash1 ^ hash2).count("1")


def find_duplicates(
    image_paths: List[Path],
    near_dup_threshold: int = 4,
) -> Dict[str, Any]:
    """
    Scans a collection of image paths and detects:
    1. Exact byte-for-byte duplicates (SHA-256 match)
    2. Visually near-identical photographs (dHash Hamming distance <= threshold)

    Returns a structured dictionary of duplicate clusters and clean image paths.
    """
    exact_hash_map: Dict[str, List[Path]] = {}
    dhash_map: Dict[Path, int] = {}
    corrupted_files: List[Path] = []

    # Step 1: Compute hashes
    for p in image_paths:
        try:
            sha = compute_exact_hash(p)
            exact_hash_map.setdefault(sha, []).append(p)

            with Image.open(p) as img:
                dhash_map[p] = compute_dhash(img)
        except Exception:
            corrupted_files.append(p)

    # Step 2: Identify exact duplicate pairs
    exact_duplicates: List[List[str]] = []
    unique_candidates: List[Path] = []

    for sha, paths in exact_hash_map.items():
        if len(paths) > 1:
            exact_duplicates.append([str(p) for p in paths])
            # Keep first as primary
            unique_candidates.append(paths[0])
        else:
            unique_candidates.append(paths[0])

    # Step 3: Identify perceptual near-duplicates among candidates
    near_duplicates: List[Tuple[str, str, int]] = []
    seen_near_pairs: Set[Tuple[str, str]] = set()

    for i in range(len(unique_candidates)):
        p1 = unique_candidates[i]
        h1 = dhash_map.get(p1)
        if h1 is None:
            continue
        for j in range(i + 1, len(unique_candidates)):
            p2 = unique_candidates[j]
            h2 = dhash_map.get(p2)
            if h2 is None:
                continue

            dist = hamming_distance(h1, h2)
            if dist <= near_dup_threshold:
                pair_key = (str(p1), str(p2))
                if pair_key not in seen_near_pairs:
                    near_duplicates.append((str(p1), str(p2), dist))
                    seen_near_pairs.add(pair_key)

    return {
        "total_scanned": len(image_paths),
        "exact_duplicates": exact_duplicates,
        "near_duplicates": near_duplicates,
        "corrupted_files": [str(p) for p in corrupted_files],
        "unique_count": len(unique_candidates) - len(seen_near_pairs),
    }
