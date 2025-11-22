# Chest X-Ray Analysis System - Complete Guide

## 🎯 Overview

This system uses AI (medgemma-27b-multimodal) to analyze chest X-ray images and detect three critical conditions:

1. **Pneumonia** - Lung infection with consolidation/infiltrates
2. **Atelectasis** - Collapsed or partially collapsed lung tissue  
3. **Fracture** - Rib, clavicle, or other bone fractures

The AI acts as an expert radiologist, examining X-rays and determining if each condition is **Present** or **Absent**.

## 📊 Dataset

- **Source**: CheXpert dataset (chexpert_train_visualCheXbert.csv)
- **Total Images**: 223,414 chest X-rays
- **Positive Cases**:
  - Pneumonia: 52,226 cases (23.4%)
  - Atelectasis: 123,924 cases (55.5%)
  - Fracture: 61,690 cases (27.6%)

## 🚀 Quick Start

### Step 1: Check LM Studio
```bash
python check_lmstudio.py
```
This verifies:
- LM Studio is running
- Server is accessible at localhost:1234
- medgemma-27b-multimodal model is loaded

### Step 2: Test Configuration
```bash
python test_xray_system.py
```
This verifies:
- Ground truth CSV loads correctly
- Target conditions exist in data
- Image files are accessible
- Shows sample data

### Step 3: Run Quick Test (3 images)
```bash
python run_quick_test.py
```
This processes 3 X-rays (one with each condition) to verify the system works end-to-end.

### Step 4: Run Full Analysis
```bash
python main.py
```
This processes multiple images (default: 10, configurable).

## 📁 File Structure

### Core Files
- **config.py** - System configuration (model, conditions, paths)
- **agents.py** - AI agents (input handler, processor, evaluator, output handler)
- **graph.py** - LangGraph workflow definition
- **main.py** - Main orchestrator for batch processing

### Test & Utility Files
- **check_lmstudio.py** - Verify LM Studio connection
- **test_xray_system.py** - Test system configuration
- **run_quick_test.py** - Quick test with 3 images

### Data Files
- **chexpert_train_visualCheXbert.csv** - Ground truth labels
- **CheXpert-v1.0/** - X-ray image files

### Results
- **results/** - Output folder for analysis results

## 🔧 Configuration

### Adjusting Number of Images

In `main.py`, line ~30:
```python
image_paths = get_image_files_from_csv(GROUND_TRUTH_CSV, limit=10)
```

Change the `limit` parameter:
- `limit=10` - Process 10 images (quick test)
- `limit=100` - Process 100 images
- `limit=1000` - Process 1,000 images
- `limit=None` - Process ALL 223,414 images (will take hours)

### Batch Processing Settings

In `main.py`, line ~37:
```python
batch_processor = BatchProcessor(batch_size=10, save_interval=5)
```

- `batch_size`: Number of images per batch
- `save_interval`: Save intermediate results every N images

## 📈 Results Format

Results are saved as CSV files in the `results/` folder:

**Filename**: `chexpert_results_YYYYMMDD_HHMMSS.csv`

**Columns**:
- `image_path` - Full path to X-ray image
- `image_name` - Filename only
- `Pneumonia_predicted` - AI prediction (Present/Absent)
- `Pneumonia_ground_truth` - True label (1.0/0.0)
- `Pneumonia_correct` - Match (True/False)
- `Atelectasis_predicted` - AI prediction
- `Atelectasis_ground_truth` - True label
- `Atelectasis_correct` - Match
- `Fracture_predicted` - AI prediction
- `Fracture_ground_truth` - True label
- `Fracture_correct` - Match

## 🎓 How the AI Analyzes X-Rays

The AI is prompted as an expert radiologist and looks for specific findings:

### Pneumonia
- Consolidation or infiltrates in lung fields
- Air space opacities
- Patchy or diffuse opacities suggesting infection

### Atelectasis
- Collapsed or partially collapsed lung tissue
- Volume loss in lung fields
- Displacement of fissures or mediastinal shift
- Linear or plate-like opacities

### Fracture
- Rib fractures (discontinuity in rib cortex)
- Clavicle fractures
- Any visible bone fractures in the chest area

## 📊 Accuracy Metrics

The system calculates accuracy **per condition**:

```
Accuracy per condition:
  Pneumonia: 8/10 (80.00%)
  Atelectasis: 9/10 (90.00%)
  Fracture: 7/10 (70.00%)
```

This is more informative than overall accuracy since:
- Each condition has different prevalence
- Some conditions are harder to detect
- Multiple conditions can be present in one image

## 🔍 Workflow

```
Input Handler → Multimodal Processor → Result Evaluator → Output Handler
     ↓                  ↓                      ↓                ↓
Load image      Analyze with AI      Compare to truth    Save results
```

1. **Input Handler**: Loads X-ray image from disk
2. **Multimodal Processor**: Sends image to AI with expert prompt
3. **Result Evaluator**: Compares AI predictions to ground truth
4. **Output Handler**: Saves results to CSV

## ⚠️ Important Notes

- **Research/Education Only**: This system is for research and educational purposes
- **Not Medical Advice**: Does NOT provide medical diagnosis or treatment recommendations
- **Requires LM Studio**: Must have LM Studio running with medgemma-27b-multimodal
- **Processing Time**: Each image takes ~5-10 seconds depending on hardware
- **Memory Usage**: Large batch processing may require significant RAM

## 🐛 Troubleshooting

### "Cannot connect to LM Studio"
- Ensure LM Studio is running
- Click the green play button to start the server
- Verify port is 1234 (default)

### "No ground truth found"
- Check that `chexpert_train_visualCheXbert.csv` exists
- Verify image paths in CSV match actual file locations

### "Image file not found"
- Ensure `CheXpert-v1.0/` folder contains the images
- Check that paths in CSV are correct

### Low accuracy
- Verify the correct model is loaded (medgemma-27b-multimodal)
- Check that the model is a multimodal vision model
- Try adjusting temperature in `agents.py` (currently 0.1)

## 📚 Additional Documentation

- **XRAY_ANALYSIS_GUIDE.md** - Detailed usage guide
- **CHANGES_SUMMARY.md** - What changed from dermatology system
- **RUN_INSTRUCTIONS.md** - Original system instructions

## 🎯 Next Steps

After running the system:

1. Review results in `results/` folder
2. Analyze per-condition accuracy
3. Identify which conditions are harder to detect
4. Adjust processing volume as needed
5. Consider fine-tuning prompts for better accuracy

---

**Ready to start?** Run `python check_lmstudio.py` to begin!
