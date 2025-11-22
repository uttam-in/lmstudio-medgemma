# 🚀 Quick Start - Chest X-Ray Analysis

## What This System Does

Analyzes chest X-rays to detect:
- ✅ **Pneumonia** (lung infection)
- ✅ **Atelectasis** (collapsed lung)
- ✅ **Fracture** (broken bones)

Uses AI (medgemma-27b-multimodal) acting as an expert radiologist.

## Run These Commands in Order

### 1️⃣ Check LM Studio is Running
```bash
python check_lmstudio.py
```
**Expected**: ✓ LM Studio is running and accessible

---

### 2️⃣ Verify System Configuration
```bash
python test_xray_system.py
```
**Expected**: 
- ✓ CSV loaded (223,414 records)
- ✓ All 3 conditions found
- ✓ Sample image exists

---

### 3️⃣ Quick Test (3 X-rays)
```bash
python run_quick_test.py
```
**Expected**: 
- Processes 3 images (one with each condition)
- Shows predictions vs ground truth
- Saves results to `results/quick_test_TIMESTAMP.csv`

---

### 4️⃣ Full Analysis (10+ X-rays)
```bash
python main.py
```
**Expected**:
- Processes 10 images (default)
- Shows accuracy per condition
- Saves results to `results/chexpert_results_TIMESTAMP.csv`

---

## Results Location

All results saved in: **`results/`** folder

Each CSV contains:
- Image path
- AI predictions (Present/Absent)
- Ground truth (1.0/0.0)
- Correctness (True/False)
- Per-condition accuracy

---

## Adjust Processing Volume

Edit `main.py` line 30:
```python
# Process 10 images (quick)
image_paths = get_image_files_from_csv(GROUND_TRUTH_CSV, limit=10)

# Process 100 images
image_paths = get_image_files_from_csv(GROUND_TRUTH_CSV, limit=100)

# Process ALL 223,414 images (takes hours!)
image_paths = get_image_files_from_csv(GROUND_TRUTH_CSV, limit=None)
```

---

## Troubleshooting

**Problem**: "Cannot connect to LM Studio"
- **Solution**: Start LM Studio and click the green play button

**Problem**: "No ground truth found"
- **Solution**: Ensure `chexpert_train_visualCheXbert.csv` exists

**Problem**: "Image file not found"
- **Solution**: Verify `CheXpert-v1.0/` folder contains images

---

## What Changed?

This system was updated from dermatology (skin lesions) to radiology (chest X-rays):

| Before | After |
|--------|-------|
| 9 skin conditions | 3 chest conditions |
| ISIC dataset | CheXpert dataset |
| Top-3 classification | Present/Absent detection |
| Overall accuracy | Per-condition accuracy |

See **CHANGES_SUMMARY.md** for full details.

---

## Need More Help?

- **Full Guide**: `README_XRAY.md`
- **Detailed Usage**: `XRAY_ANALYSIS_GUIDE.md`
- **Changes Made**: `CHANGES_SUMMARY.md`

---

**Ready?** Start with: `python check_lmstudio.py`
