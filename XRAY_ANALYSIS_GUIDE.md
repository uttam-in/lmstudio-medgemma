# Chest X-Ray Analysis System

## Overview
This system analyzes chest X-ray images to detect three key conditions:
- **Pneumonia**: Lung infection with consolidation/infiltrates
- **Atelectasis**: Collapsed or partially collapsed lung tissue
- **Fracture**: Rib, clavicle, or other bone fractures

## Configuration

### Ground Truth Data
- **File**: `chexpert_train_visualCheXbert.csv`
- **Total Records**: 223,414 chest X-rays
- **Positive Cases**:
  - Pneumonia: 52,226 cases
  - Atelectasis: 123,924 cases
  - Fracture: 61,690 cases

### System Settings (config.py)
- **Model**: medgemma-27b-multimodal (via LM Studio)
- **Target Conditions**: Pneumonia, Atelectasis, Fracture
- **Results Path**: `results/` folder

## How to Run

### 1. Test Configuration
```bash
python test_xray_system.py
```
This verifies:
- Ground truth CSV is loaded correctly
- Target conditions exist in the data
- Image files are accessible
- Sample data is displayed

### 2. Run Analysis
```bash
python main.py
```

The system will:
1. Load ground truth labels from CSV
2. Create the LangGraph workflow
3. Process X-ray images (starts with 10 for testing)
4. For each image, the AI will analyze and determine if each condition is Present or Absent
5. Compare predictions against ground truth
6. Save results to `results/chexpert_results_TIMESTAMP.csv`

### 3. View Results
Results are saved in the `results/` folder with columns:
- `image_path`: Path to the X-ray image
- `image_name`: Filename
- `Pneumonia_predicted`: AI prediction (Present/Absent)
- `Pneumonia_ground_truth`: True label (1.0/0.0)
- `Pneumonia_correct`: Whether prediction matches truth
- (Same for Atelectasis and Fracture)

## Expert Radiologist Prompt

The AI acts as an expert radiologist and looks for:

**Pneumonia**:
- Consolidation or infiltrates in lung fields
- Air space opacities
- Patchy or diffuse opacities suggesting infection

**Atelectasis**:
- Collapsed or partially collapsed lung tissue
- Volume loss in lung fields
- Displacement of fissures or mediastinal shift
- Linear or plate-like opacities

**Fracture**:
- Rib fractures (discontinuity in rib cortex)
- Clavicle fractures
- Any visible bone fractures in the chest area

## Adjusting Processing Volume

In `main.py`, line ~30:
```python
image_paths = get_image_files_from_csv(GROUND_TRUTH_CSV, limit=10)
```

Change `limit=10` to:
- `limit=100` for 100 images
- `limit=None` for all 223,414 images (will take significant time)

## Output Format

The AI returns predictions in JSON format:
```json
{
    "Pneumonia": "Present" or "Absent",
    "Atelectasis": "Present" or "Absent",
    "Fracture": "Present" or "Absent"
}
```

## Notes
- This system is for **research and educational purposes only**
- Does NOT provide medical advice, diagnosis, or treatment recommendations
- Requires LM Studio running with medgemma-27b-multimodal model
- Results include per-condition accuracy metrics
