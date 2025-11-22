# Chest X-Ray Analysis System

An AI-powered system built with LangGraph that analyzes chest X-ray images to detect Pneumonia, Atelectasis, and Fracture using a multimodal LLM (medgemma-27b-multimodal) running on LM Studio. The AI acts as an expert radiologist, examining X-rays and determining if each condition is Present or Absent.

## 🎯 Target Conditions

The system detects three critical chest conditions:

1. **Pneumonia** - Lung infection with consolidation/infiltrates
2. **Atelectasis** - Collapsed or partially collapsed lung tissue
3. **Fracture** - Rib, clavicle, or other bone fractures

## 📊 Dataset

- **Source**: CheXpert (chexpert_train_visualCheXbert.csv)
- **Total Images**: 223,414 chest X-rays
- **Positive Cases**:
  - Pneumonia: 52,226 (23.4%)
  - Atelectasis: 123,924 (55.5%)
  - Fracture: 61,690 (27.6%)

## 🏗️ Architecture

The system follows a multi-agent LangGraph workflow:

```
Input Handler → Multimodal Processor → Result Evaluator → Output Handler
                        ↓
            Expert Radiologist AI
        (medgemma-27b-multimodal via LM Studio)
```

### Agents

1. **Input Handler**: Loads X-ray images and checks file existence
2. **Multimodal Processor**: Analyzes images with AI radiologist prompt
3. **Result Evaluator**: Compares AI predictions with ground truth
4. **Output Handler**: Stores results with per-condition accuracy

## 🚀 Quick Start

### Prerequisites

1. **LM Studio** running locally on port 1234
2. **medgemma-27b-multimodal** model loaded in LM Studio
3. Python 3.8+
4. CheXpert dataset with images in `CheXpert-v1.0/` folder

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Quick Test (Recommended)

```bash
# 1. Check LM Studio connection
python check_lmstudio.py

# 2. Verify system configuration
python test_xray_system.py

# 3. Check file existence
python test_skip_missing.py

# 4. Quick test with 3 images
python run_quick_test.py

# 5. Set processing limit (interactive)
python set_processing_limit.py

# 6. Run analysis
python main.py
```

## 💻 Usage

### Process All Images (Default)

```bash
python main.py
```

**Default Configuration**:
- Processes ALL 223,414 images (~18 days)
- Progress updates every 10 images
- Auto-saves every 100 images
- Automatically skips missing files

### Adjust Processing Volume

Use the interactive script:
```bash
python set_processing_limit.py
```

Or manually edit `main.py` line 30:
```python
# Quick test (100 images, ~12 minutes)
image_paths = get_image_files_from_csv(GROUND_TRUTH_CSV, limit=100)

# Small test (1,000 images, ~2 hours)
image_paths = get_image_files_from_csv(GROUND_TRUTH_CSV, limit=1000)

# Full dataset (223,414 images, ~18 days)
image_paths = get_image_files_from_csv(GROUND_TRUTH_CSV, limit=None)
```

### What the System Does

1. Loads ground truth from CSV (223,414 records)
2. Creates LangGraph workflow
3. For each X-ray image:
   - Checks if file exists (skips if missing)
   - Loads image from disk
   - Sends to AI with expert radiologist prompt
   - AI determines: Present or Absent for each condition
   - Compares to ground truth
   - Calculates per-condition accuracy
4. Saves results every 100 images
5. Generates final summary with statistics

### Output Files

All results are saved in the `results/` folder:

- `chexpert_results_TIMESTAMP.csv` - Complete results with predictions
- `results_temp.csv` - Intermediate saves (every 100 images)

## 🩺 Expert Radiologist Prompt

The AI analyzes X-rays looking for specific findings:

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

## 📋 Output Format

### AI Predictions (JSON)
```json
{
    "Pneumonia": "Present" or "Absent",
    "Atelectasis": "Present" or "Absent",
    "Fracture": "Present" or "Absent"
}
```

### Results CSV Columns
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

## 📁 Core Files

### Main System
- `main.py` - Main orchestrator with batch processing
- `graph.py` - LangGraph workflow definition
- `agents.py` - AI agents (Input Handler, Processor, Evaluator, Output Handler)
- `config.py` - Configuration, prompts, and paths
- `batch_processor.py` - Progress tracking and batch management

### Test & Utility Scripts
- `check_lmstudio.py` - Verify LM Studio connection
- `test_xray_system.py` - Test system configuration
- `test_skip_missing.py` - Check file existence
- `run_quick_test.py` - Quick 3-image test
- `set_processing_limit.py` - Interactive limit setter

### Data Files
- `chexpert_train_visualCheXbert.csv` - Ground truth labels (223,414 records)
- `CheXpert-v1.0/` - X-ray image files

## 📊 Results & Metrics

### Console Output Example
```
Total images in CSV: 223414
Images processed: 223414
Images skipped (not found): 0
⏱ Total processing time: 435.50 hours (26130.0 minutes)
⚡ Average time per image: 7.02 seconds

📊 Final Accuracy per condition:
  Pneumonia: 180000/223414 (80.56%)
  Atelectasis: 195000/223414 (87.28%)
  Fracture: 170000/223414 (76.09%)

✓ Results saved to: results/chexpert_results_20241122_143022.csv
```

### Key Features

✅ **Per-Condition Accuracy** - Separate metrics for each condition
✅ **Automatic Skip** - Missing files are skipped automatically
✅ **Progress Tracking** - Updates every 10 images
✅ **Auto-Save** - Results saved every 100 images
✅ **Error Handling** - Comprehensive error management
✅ **Time Estimates** - Processing time and ETA
✅ **Detailed Statistics** - Complete performance metrics

## ⏱ Processing Time

| Images | Time | Use Case |
|--------|------|----------|
| 100 | ~12 minutes | Quick verification |
| 1,000 | ~2 hours | Initial accuracy estimate |
| 10,000 | ~20 hours | Better accuracy estimate |
| 50,000 | ~4 days | Large-scale test |
| 223,414 | ~18 days | Complete analysis |

*Based on 7 seconds per image average*


## 📚 Documentation

Comprehensive documentation is available:

| Document | Purpose |
|----------|---------|
| **START_HERE.md** | Quick overview and getting started |
| **QUICK_START.md** | Step-by-step instructions |
| **README_XRAY.md** | Complete system documentation |
| **RUN_FULL_ANALYSIS.md** | Guide for processing all images |
| **SYSTEM_ARCHITECTURE.md** | Technical architecture details |
| **SKIP_MISSING_FILES_UPDATE.md** | Automatic skip feature |
| **LATEST_UPDATES.md** | Recent changes and updates |
| **QUICK_REFERENCE.txt** | One-page quick reference |

## 🔧 Configuration

### LM Studio Setup

1. Start LM Studio
2. Load the `medgemma-27b-multimodal` model
3. Enable the local server on `http://localhost:1234`
4. Ensure multimodal/vision capabilities are enabled
5. Click the green play button to start server

### Adjust Processing Volume

**Method 1 - Interactive (Recommended)**:
```bash
python set_processing_limit.py
```

**Method 2 - Manual Edit**:
Edit `main.py` line 30 to change the limit value

## 🚨 Troubleshooting

### Common Issues

**"Cannot connect to LM Studio"**
- Start LM Studio and click the green play button
- Verify server is running on port 1234
- Check firewall settings

**"No ground truth found"**
- Verify `chexpert_train_visualCheXbert.csv` exists
- Check CSV format and columns

**"Image file not found"**
- Ensure `CheXpert-v1.0/` folder contains images
- Run `python test_skip_missing.py` to check files
- System will automatically skip missing files

**Low accuracy**
- Verify correct model is loaded (medgemma-27b-multimodal)
- Ensure model supports multimodal/vision
- Check that images are loading correctly

## 🎯 Recommended Workflow

### Phase 1: Verification (5 minutes)
```bash
python check_lmstudio.py      # Verify LM Studio
python test_xray_system.py    # Verify configuration
python test_skip_missing.py   # Check files
```

### Phase 2: Quick Test (2 minutes)
```bash
python run_quick_test.py      # Test with 3 images
```

### Phase 3: Small Test (~12 minutes)
```bash
python set_processing_limit.py  # Select 100 images
python main.py
```

### Phase 4: Medium Test (~2 hours)
```bash
python set_processing_limit.py  # Select 1,000 images
python main.py
```

### Phase 5: Full Analysis (~18 days)
```bash
python set_processing_limit.py  # Select ALL images
python main.py
```

## 💡 Tips for Long-Running Process

1. **Start Small** - Test with 100-1,000 images first
2. **Monitor Progress** - Check intermediate results regularly
3. **Keep System Awake** - Adjust power settings
4. **Use Screen/Tmux** - For remote sessions (Linux/Mac)
5. **Check Resources** - Monitor CPU/RAM usage
6. **Verify Model** - Ensure correct model stays loaded

## 🔍 System Requirements

### Hardware
- **CPU**: Multi-core recommended
- **RAM**: 4-8 GB minimum
- **Disk**: 50+ MB for results
- **GPU**: Optional (if LM Studio supports)

### Software
- **Python**: 3.8+
- **LM Studio**: Latest version
- **Model**: medgemma-27b-multimodal
- **OS**: Windows, Linux, or macOS

## 📈 Expected Accuracy

Based on CheXpert dataset characteristics:

| Condition | Prevalence | Expected Accuracy |
|-----------|------------|-------------------|
| Pneumonia | 23.4% | 75-85% |
| Atelectasis | 55.5% | 80-90% |
| Fracture | 27.6% | 70-80% |

*Actual accuracy depends on model performance*

## ⚠️ Important Notes

- **Research/Education Only**: This system is for research and educational purposes
- **Not Medical Advice**: Does NOT provide medical diagnosis or treatment recommendations
- **Requires LM Studio**: Must have LM Studio running with correct model
- **Processing Time**: Full dataset takes approximately 18 days
- **Automatic Skip**: Missing files are skipped automatically without crashing

## 🤝 Contributing

This is a research/educational project. Feel free to:
- Test with different models
- Adjust prompts for better accuracy
- Add more conditions
- Implement parallel processing
- Create visualizations

## 📝 License

This project is for research and educational purposes only.

## 🎉 Features Summary

✅ Expert radiologist AI prompt
✅ Per-condition accuracy tracking
✅ Automatic intermediate saves
✅ Progress monitoring every 10 images
✅ Easy limit adjustment
✅ Comprehensive error handling
✅ Automatic skip for missing files
✅ Detailed result statistics
✅ Complete documentation
✅ Interactive configuration

## 🚀 Getting Started

**Quickest way to start**:

```bash
# 1. Verify everything is ready
python check_lmstudio.py
python test_xray_system.py

# 2. Run quick test
python run_quick_test.py

# 3. Set your desired limit
python set_processing_limit.py

# 4. Start analysis
python main.py
```

**For detailed guidance**, read: `START_HERE.md`

---

**Status**: ✅ Production Ready
**Last Updated**: November 22, 2024
**Version**: 2.0 (Chest X-Ray Analysis)
