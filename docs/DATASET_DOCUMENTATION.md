# 📊 Smart Jasmine Farming Assistant: Dataset Documentation

**Crop:** *Jasminum sambac* (Gundu Malli / குண்டு மல்லி)  
**Taxonomy:** 4 Discrete Maturity and Quality Stages  
**Partitioning:** Leakage-Safe 70% Train / 15% Validation / 15% Test  

---

## 1. Directory Structure

```
data/
├── raw/
│   ├── single_buds/
│   │   ├── READY_TO_PLUCK/          # Commercially mature tight white buds
│   │   ├── NOT_READY/               # Immature green or compact tight buds
│   │   ├── TOO_OPEN/                # Over-open / bloomed flowers
│   │   └── DAMAGED_OR_ABNORMAL/     # Pores, bud worm frass, rot, webbed buds
│   └── whole_plant/
│       └── incoming/                # Segregated canopy photos (Reserved for Phase 7 YOLO)
└── processed/
    ├── train/                       # 70% Leakage-free training split
    ├── val/                         # 15% Validation split for model checkpointing
    ├── test/                        # 15% Independent test split for unbiased evaluation
    └── dataset_manifest.json        # Partition tracking manifest with hash signatures
```

---

## 2. 4-Class Flower Maturity Taxonomy

| Class Label | Tamil Term | Botanical & Visual Indicators | Commercial Market Value |
|---|---|---|---|
| `READY_TO_PLUCK` | பறிக்கத் தயார் | Corolla tube elongated; petals creamy white, firm, and fully closed. Stalk green and firm. | **Grade A (Premium):** Highest commercial market price. Retains fragrance oils during transport. |
| `NOT_READY` | முதிரவில்லை | Corolla tube unelongated; calyx tight; petals predominantly greenish or pale green. | **Immature:** Severely penalized; experiences post-harvest weight loss and fails to open properly. |
| `TOO_OPEN` | மலர்ந்துவிட்டது | Petals unfurled, exposing anthers and stigma. Essential oils rapidly volatilizing. | **Grade C:** Bruises brown during transport; suitable only for immediate home puja or local garlands. |
| `DAMAGED_OR_ABNORMAL` | சேதமடைந்தது | Pinhead bore holes (*Hendecasis* frass), silken webbing, midge necrosis, or fungal rot. | **Rejected:** Non-marketable; must be culled and destroyed to halt pest cycles in the garden. |

---

## 3. Data Leakage Prevention & Partitioning Pipeline

In agricultural computer vision, sequential burst-shot photographs of the same flower bud from slightly different angles share near-identical features. Splitting them randomly across training and test sets produces **perceptual data leakage**, inflating test accuracy artificially while performing poorly in the field.

### Dual-Layer Duplicate Detector ([src/dataset/duplicate_detector.py](file:///C:/Users/m.sathish/.gemini/antigravity-ide/scratch/smart-jasmine-assistant/src/dataset/duplicate_detector.py)):
1. **Exact Byte Matching (SHA-256):** Computes cryptographic hash to eliminate exact duplicate uploads.
2. **Perceptual Difference Hashing (dHash):** Computes a 64-bit gradient hash by resizing to $9 \times 8$ grayscale and comparing adjacent horizontal pixels. Pairs with Hamming distance $\le 4$ are flagged as burst-shot near-duplicates.

### Partitioning Rules ([src/dataset/organizer.py](file:///C:/Users/m.sathish/.gemini/antigravity-ide/scratch/smart-jasmine-assistant/src/dataset/organizer.py)):
- All connected duplicate/near-duplicate clusters are placed into the **same partition** (`train`, `val`, or `test`).
- Partitions maintain a 70% / 15% / 15% stratified balance across all 4 maturity classes.
- Generates `dataset_manifest.json` recording every image's source path, split assignment, SHA-256 hash, and dHash signature.

---

## 4. Whole-Plant Canopy Photo Segregation

Whole-plant bush photographs contain multiple overlapping buds under complex canopy shadows. Feeding whole-bush photos into single-bud classifiers causes label ambiguity and severe background noise.
- All whole-plant photographs are automatically routed to `data/raw/whole_plant/incoming/`.
- They are **strictly excluded** from single-bud MobileNetV2 classification.
- They are reserved for **Phase 7 Multi-Bud Object Detection (YOLO)** with bounding box annotations.

---

## 5. Field Photography Guidelines for the Family Farm

Growers must observe the following field protocol when gathering photos:
1. **Morning Lighting Window:** Capture between **6:30 AM and 9:00 AM** in natural diffused morning sunlight. Avoid harsh midday direct sunlight (which creates bleaching highlights) or flash photography (which distorts petal color).
2. **Camera Distance & Framing:** Frame single buds $10\text{--}15\text{ cm}$ away, centered in focus, with the stalk visible.
3. **Background Contrast:** Use natural foliage or place a hand/dark board behind the bud to ensure sharp edge definition against the corolla tube.
4. **Variety & Angles:** Capture variations across different garden sections, younger vs older bushes, and cloudy vs clear morning conditions.
