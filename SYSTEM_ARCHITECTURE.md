# System Architecture - Chest X-Ray Analysis

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  CHEST X-RAY ANALYSIS SYSTEM                    │
│                                                                 │
│  Purpose: Detect Pneumonia, Atelectasis, Fracture in X-rays   │
│  Model: medgemma-27b-multimodal (via LM Studio)               │
│  Dataset: CheXpert (223,414 images)                           │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌──────────────────┐
│  Ground Truth    │
│  CSV File        │
│  (223,414 rows)  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Image Paths     │
│  Extraction      │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│                    LANGGRAPH WORKFLOW                        │
│                                                              │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   │
│  │    Input     │   │  Multimodal  │   │   Result     │   │
│  │   Handler    │──▶│  Processor   │──▶│  Evaluator   │   │
│  └──────────────┘   └──────────────┘   └──────────────┘   │
│         │                   │                   │          │
│    Load Image        Analyze with AI      Compare to      │
│    from Disk         (Expert Radiologist)  Ground Truth   │
│                                                            │
│                           │                                │
│                           ▼                                │
│                  ┌──────────────┐                         │
│                  │   Output     │                         │
│                  │   Handler    │                         │
│                  └──────────────┘                         │
│                           │                                │
└───────────────────────────┼────────────────────────────────┘
                            │
                            ▼
                   ┌──────────────┐
                   │   Results    │
                   │   CSV File   │
                   └──────────────┘
```

## Component Details

### 1. Input Handler (agents.py)
```python
Input:  image_path (string)
Output: image_data (bytes), image_name (string)
Action: Loads X-ray image from disk
```

### 2. Multimodal Processor (agents.py)
```python
Input:  image_data (bytes)
Output: prediction (dict)
Action: 
  - Encodes image to base64
  - Sends to LM Studio with expert radiologist prompt
  - Receives JSON response:
    {
      "Pneumonia": "Present" or "Absent",
      "Atelectasis": "Present" or "Absent",
      "Fracture": "Present" or "Absent"
    }
```

### 3. Result Evaluator (agents.py)
```python
Input:  prediction (dict), image_path (string)
Output: ground_truth (dict), evaluation (dict)
Action:
  - Looks up ground truth from CSV
  - Compares each condition prediction to truth
  - Returns per-condition correctness
```

### 4. Output Handler (agents.py)
```python
Input:  Complete state
Output: Final state (unchanged)
Action: Pass-through for future extensions
```

## Configuration (config.py)

```python
# Model Settings
LMSTUDIO_BASE_URL = "http://localhost:1234/v1"
MODEL_NAME = "medgemma-27b-multimodal"

# Target Conditions
TARGET_CONDITIONS = ["Pneumonia", "Atelectasis", "Fracture"]

# Paths
CHEXPERT_PATH = "CheXpert-v1.0"
GROUND_TRUTH_CSV = "chexpert_train_visualCheXbert.csv"
RESULTS_PATH = "results"

# Expert Radiologist Prompt
SYSTEM_PROMPT = """
You are an expert radiologist analyzing chest X-rays...
[Detailed instructions for each condition]
"""
```

## State Management

```python
State = {
    "image_path": str,           # Path to X-ray image
    "image_name": str,           # Filename only
    "image_data": bytes,         # Raw image data
    "prediction": {              # AI predictions
        "Pneumonia": "Present/Absent",
        "Atelectasis": "Present/Absent",
        "Fracture": "Present/Absent"
    },
    "ground_truth": {            # True labels
        "Pneumonia": 1.0 or 0.0,
        "Atelectasis": 1.0 or 0.0,
        "Fracture": 1.0 or 0.0
    },
    "evaluation": {              # Correctness
        "Pneumonia": True/False,
        "Atelectasis": True/False,
        "Fracture": True/False
    },
    "error": str                 # Error message if any
}
```

## Batch Processing (main.py)

```
For each image in dataset:
  1. Create initial state
  2. Run through workflow
  3. Collect results
  4. Update progress
  5. Save intermediate results every N images
  
After all images:
  1. Calculate per-condition accuracy
  2. Save final results to CSV
  3. Display summary
```

## Results Format

```csv
image_path,image_name,Pneumonia_predicted,Pneumonia_ground_truth,Pneumonia_correct,Atelectasis_predicted,Atelectasis_ground_truth,Atelectasis_correct,Fracture_predicted,Fracture_ground_truth,Fracture_correct
CheXpert-v1.0/train/patient00002/study1/view1_frontal.jpg,view1_frontal.jpg,Present,1.0,True,Present,1.0,True,Present,1.0,True
```

## Accuracy Calculation

```python
For each condition:
  correct_count = sum(evaluation[condition] == True)
  total_count = len(results)
  accuracy = (correct_count / total_count) * 100
```

Example output:
```
Accuracy per condition:
  Pneumonia: 8/10 (80.00%)
  Atelectasis: 9/10 (90.00%)
  Fracture: 7/10 (70.00%)
```

## Key Design Decisions

### Why Per-Condition Evaluation?
- Each condition has different prevalence in dataset
- Multiple conditions can exist in one image
- More informative than single overall accuracy

### Why Present/Absent vs Probability?
- Simpler for model to output
- Easier to evaluate against binary ground truth
- More interpretable for users

### Why LangGraph?
- Clear workflow visualization
- Easy to add/modify nodes
- Built-in state management
- Supports complex agent interactions

## File Dependencies

```
main.py
  ├── config.py (settings)
  ├── graph.py (workflow)
  ├── agents.py (AI agents)
  │     └── config.py
  └── batch_processor.py (progress tracking)

test_xray_system.py
  └── config.py

run_quick_test.py
  ├── config.py
  ├── graph.py
  └── agents.py

check_lmstudio.py
  └── config.py
```

## External Dependencies

- **LM Studio**: Local AI model server
- **medgemma-27b-multimodal**: Vision-language model
- **LangChain**: LLM framework
- **LangGraph**: Workflow orchestration
- **Pandas**: Data manipulation
- **PIL**: Image processing

## Performance Considerations

- **Processing Time**: ~5-10 seconds per image
- **Memory Usage**: ~2-4 GB for model + image data
- **Batch Size**: Configurable (default: 10)
- **Save Interval**: Intermediate saves every N images
- **Total Dataset**: 223,414 images = ~300-500 hours for full run

## Future Enhancements

1. **Parallel Processing**: Process multiple images simultaneously
2. **Confidence Scores**: Add probability outputs
3. **Visualization**: Generate heatmaps showing areas of interest
4. **Additional Conditions**: Expand beyond 3 conditions
5. **Model Comparison**: Test different AI models
6. **Error Analysis**: Detailed analysis of misclassifications
