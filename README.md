# Dermatology Image Classification System

An agentic system built with LangGraph that classifies dermatology images using a multimodal LLM (medgemma-27b-multimodal) running on LM Studio.

## Architecture

The system follows a multi-agent workflow:

```
Orchestrator
    ↓
Input Handler → Multimodal Processor → Result Evaluator → Output Handler
                        ↓
                Generative AI LLM (medgemma-27b-multimodal via LM Studio)
```

### Agents

1. **Input Handler**: Loads and preprocesses images
2. **Multimodal Processor**: Sends images to LM Studio for classification
3. **Result Evaluator**: Compares predictions with ground truth
4. **Output Handler**: Stores and formats results
5. **Orchestrator**: Coordinates the entire workflow

## Setup

### Prerequisites

1. **LM Studio** running locally on port 1234
2. **medgemma-27b-multimodal** model loaded in LM Studio
3. Python 3.9+

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### LM Studio Configuration

1. Start LM Studio
2. Load the `medgemma-27b-multimodal` model
3. Enable the local server on `http://localhost:1234`
4. Ensure multimodal/vision capabilities are enabled

## Usage

Run the classification system on the full dataset:

```bash
python main.py
```

The system will:
- Load all images from the `archive/` folder
- Process each image through the LangGraph workflow with progress tracking
- Generate top-3 predictions for each image
- Evaluate accuracy against ground truth
- Save intermediate results every 100 images
- Generate comprehensive visualizations and metrics

### Output Files

All results are saved in the `results/` folder with timestamps:

- `results_TIMESTAMP.csv` - Detailed predictions for all images
- `architecture_TIMESTAMP.png` - System architecture diagram
- `confusion_matrix_TIMESTAMP.png` - Confusion matrix heatmap
- `roc_curves_TIMESTAMP.png` - ROC curves for all classes
- `auc_scores_TIMESTAMP.txt` - AUC scores by category
- `performance_metrics_TIMESTAMP.txt` - Detailed classification report
- `accuracy_comparison_TIMESTAMP.png` - Top-1 vs Top-3 accuracy chart

## Classification Categories

- **MEL**: Melanoma
- **NV**: Melanocytic nevus
- **BCC**: Basal cell carcinoma
- **AK**: Actinic keratosis
- **BKL**: Benign keratosis
- **DF**: Dermatofibroma
- **VASC**: Vascular lesion
- **SCC**: Squamous cell carcinoma
- **UNK**: Unknown

## Output Format

Predictions are returned as JSON:
```json
{
    "top_1": "MEL",
    "top_2": "NV",
    "top_3": "BCC"
}
```

A prediction is considered correct if the ground truth matches any of the top 3 predictions.

## Files

- `main.py`: Orchestrator that coordinates the workflow
- `graph.py`: LangGraph workflow definition
- `agents.py`: Individual agent implementations (Input Handler, Processor, Evaluator, Output Handler)
- `config.py`: Configuration and prompts
- `visualizations.py`: Generate all charts, graphs, and metrics
- `batch_processor.py`: Batch processing with progress tracking
- `requirements.txt`: Python dependencies

## Results

Results are saved in CSV format with columns:
- `image`: Image filename
- `ground_truth`: True label
- `top_1`, `top_2`, `top_3`: Predicted labels
- `correct`: Boolean indicating if prediction was correct

### Visualizations

The system automatically generates:

1. **Architecture Diagram**: Visual representation of the LangGraph workflow
2. **Confusion Matrix**: Shows classification performance across all categories
3. **ROC Curves**: Multi-class ROC curves with AUC scores for each category
4. **Performance Metrics**: Precision, recall, F1-score for each class
5. **Accuracy Comparison**: Bar chart comparing Top-1 vs Top-3 accuracy

### Performance Tracking

- Real-time progress bar with ETA
- Processing rate (images/second)
- Intermediate results saved every 100 images
- Error tracking and recovery
