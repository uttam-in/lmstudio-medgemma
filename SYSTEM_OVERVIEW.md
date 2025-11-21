# Dermatology Image Classification System - Technical Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATOR                             │
│                    (LangGraph StateGraph)                        │
└────────────┬────────────────────────────────────────────────────┘
             │
             ├──► [1] Input Handler
             │    └─ Load & preprocess images
             │    └─ Extract image metadata
             │
             ├──► [2] Multimodal Media Processor
             │    └─ Encode image to base64
             │    └─ Send to LM Studio API
             │    └─ Parse JSON predictions
             │         │
             │         ├──► Generative AI LLM
             │         │    (medgemma-27b-multimodal)
             │         │    via LM Studio
             │         │
             │         └──► Returns: {"top_1": "MEL", "top_2": "NV", "top_3": "BCC"}
             │
             ├──► [3] Result Evaluator
             │    └─ Compare with ground truth
             │    └─ Calculate accuracy (top-3)
             │    └─ Track performance metrics
             │
             └──► [4] Output Handler
                  └─ Store results to CSV
                  └─ Generate visualizations
```

## Agent Workflow

### State Management

Each image flows through the system with a shared state:

```python
State = {
    "image_path": str,        # Path to image file
    "image_name": str,        # Image identifier
    "image_data": bytes,      # Raw image data
    "prediction": dict,       # {"top_1": "MEL", "top_2": "NV", "top_3": "BCC"}
    "ground_truth": str,      # True label from CSV
    "is_correct": bool,       # True if ground_truth in [top_1, top_2, top_3]
    "error": str             # Error message if any
}
```

### Agent Responsibilities

#### 1. Input Handler
- **Input**: Image file path
- **Process**: Load image, read bytes, extract filename
- **Output**: Updated state with image_data and image_name

#### 2. Multimodal Processor
- **Input**: Image data from state
- **Process**: 
  - Encode image to base64
  - Create multimodal message with system prompt
  - Send to LM Studio API (medgemma-27b-multimodal)
  - Parse JSON response
- **Output**: Updated state with prediction dict

#### 3. Result Evaluator
- **Input**: Prediction and image name
- **Process**:
  - Lookup ground truth from CSV
  - Check if ground_truth matches any of top_1, top_2, or top_3
  - Set is_correct flag
- **Output**: Updated state with ground_truth and is_correct

#### 4. Output Handler
- **Input**: Complete state
- **Process**: Store results (handled by orchestrator)
- **Output**: Final state

## Classification System

### Categories (9 classes)

| Code | Description | Type |
|------|-------------|------|
| MEL  | Melanoma | Malignant |
| NV   | Melanocytic nevus | Benign |
| BCC  | Basal cell carcinoma | Malignant |
| AK   | Actinic keratosis | Precancerous |
| BKL  | Benign keratosis | Benign |
| DF   | Dermatofibroma | Benign |
| VASC | Vascular lesion | Benign |
| SCC  | Squamous cell carcinoma | Malignant |
| UNK  | Unknown | N/A |

### Evaluation Metrics

**Top-3 Accuracy**: A prediction is correct if the ground truth label appears in any of the top 3 predictions.

**Formula**: 
```
Accuracy = (Correct Predictions / Total Predictions) × 100%
where Correct = ground_truth ∈ {top_1, top_2, top_3}
```

## LLM Integration

### LM Studio Configuration

- **Endpoint**: `http://localhost:1234/v1`
- **Model**: medgemma-27b-multimodal
- **API**: OpenAI-compatible
- **Temperature**: 0.1 (low for consistent predictions)

### Prompt Engineering

The system uses a carefully crafted prompt that:
1. Defines the research/education context
2. Lists all 9 categories with descriptions
3. Specifies strict JSON output format
4. Prohibits medical advice or explanations
5. Requires exactly 3 ranked predictions

### Response Format

```json
{
    "top_1": "MEL",
    "top_2": "NV", 
    "top_3": "BCC"
}
```

## Performance Features

### Batch Processing

- **Progress Tracking**: Real-time progress bar with ETA
- **Rate Monitoring**: Images processed per second
- **Error Recovery**: Continues processing on individual failures
- **Intermediate Saves**: Results saved every 100 images

### Visualization Suite

1. **Architecture Diagram** (Graphviz)
   - Visual representation of agent workflow
   - Shows data flow and LLM integration

2. **Confusion Matrix** (Seaborn heatmap)
   - 9×9 matrix showing true vs predicted labels
   - Color-coded for easy interpretation

3. **ROC Curves** (Matplotlib)
   - One curve per class
   - AUC score for each category
   - Comparison against random classifier

4. **Performance Metrics** (Text report)
   - Precision, Recall, F1-score per class
   - Support (sample count) per class
   - Overall accuracy metrics

5. **Accuracy Comparison** (Bar chart)
   - Top-1 vs Top-3 accuracy by category
   - Sample counts displayed
   - Visual performance comparison

## Data Flow

```
archive/
├── MEL/
│   ├── ISIC_0000002.jpg ──┐
│   ├── ISIC_0000004.jpg   │
│   └── ...                │
├── NV/                    │
├── BCC/                   │
└── ...                    │
                           │
                           ├──► Input Handler
                           │
archive/                   │
└── ISIC_2019_Training_GroundTruth.csv ──┐
                                         │
                                         ├──► Result Evaluator
                                         │
                                         ▼
                                    Orchestrator
                                         │
                                         ▼
results/
├── results_TIMESTAMP.csv
├── architecture_TIMESTAMP.png
├── confusion_matrix_TIMESTAMP.png
├── roc_curves_TIMESTAMP.png
├── auc_scores_TIMESTAMP.txt
├── performance_metrics_TIMESTAMP.txt
└── accuracy_comparison_TIMESTAMP.png
```

## Technology Stack

- **LangGraph**: Agent orchestration and state management
- **LangChain**: LLM integration and message handling
- **LM Studio**: Local LLM inference server
- **medgemma-27b-multimodal**: Vision-language model for medical images
- **Pandas**: Data manipulation and CSV handling
- **Matplotlib/Seaborn**: Visualization generation
- **Scikit-learn**: Metrics calculation (confusion matrix, ROC, AUC)
- **Graphviz**: Architecture diagram generation
- **Pillow**: Image processing

## Scalability

The system is designed to handle large datasets:

- **Streaming Processing**: Images processed one at a time (memory efficient)
- **Batch Checkpointing**: Intermediate results saved periodically
- **Error Isolation**: Individual failures don't stop the workflow
- **Progress Monitoring**: Real-time feedback on processing status
- **Resumable**: Can restart from intermediate checkpoints

## Accuracy Considerations

The system uses **Top-3 accuracy** because:

1. Medical image classification is inherently uncertain
2. Multiple conditions can have similar visual presentations
3. Top-3 provides a more realistic evaluation metric
4. Clinically relevant (differential diagnosis typically includes multiple possibilities)

## Future Enhancements

Potential improvements:

- [ ] Confidence scores for each prediction
- [ ] Ensemble methods (multiple models)
- [ ] Active learning for uncertain cases
- [ ] Attention visualization (what the model looks at)
- [ ] Multi-GPU support for faster processing
- [ ] Web interface for interactive classification
- [ ] Model fine-tuning on domain-specific data
