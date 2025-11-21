# Running the Full Dataset Classification

## Quick Start

### 1. Verify LM Studio is Running

Before running the full dataset, ensure:

```bash
# Check if LM Studio server is accessible
curl http://localhost:1234/v1/models
```

You should see a response with the loaded model information.

### 2. Test with Sample Data (Recommended)

Run a quick test with 20 images first:

```bash
python run_sample.py
```

Expected output:
- Processing 20 images
- ~90% accuracy
- Completes in 1-2 minutes

### 3. Run Full Dataset

Once the sample test passes:

```bash
python main.py
```

## What to Expect

### Dataset Size

Based on your archive structure:
- **MEL**: ~4,522 images
- **NV**: ~12,875 images  
- **BCC**: ~3,323 images
- **AK**: ~867 images
- **BKL**: ~2,624 images
- **DF**: ~239 images
- **VASC**: ~253 images
- **SCC**: ~628 images

**Total**: ~25,331 images

### Processing Time Estimates

Assuming ~2-3 seconds per image with medgemma-27b-multimodal:

| Images | Time Estimate |
|--------|---------------|
| 100    | 3-5 minutes   |
| 1,000  | 30-50 minutes |
| 10,000 | 5-8 hours     |
| 25,331 | 14-21 hours   |

**Recommendation**: Run overnight or on a dedicated machine.

### Progress Monitoring

The system displays real-time progress:

```
[1234/25331] ████████████░░░░░░░░░░░░░░░░ 48.7% ✓ ISIC_0012345 | Rate: 2.3 img/s | ETA: 2h 45m
```

- Current/Total images processed
- Progress bar with percentage
- ✓ (correct) or ✗ (incorrect) indicator
- Current image name
- Processing rate (images/second)
- Estimated time remaining

### Intermediate Saves

Results are automatically saved every 100 images to:
```
results/results_temp.csv
```

If the process is interrupted, you can resume by modifying `main.py` to skip already-processed images.

## Output Files

After completion, you'll find in the `results/` folder:

### 1. Main Results CSV
```
results/results_20251120_HHMMSS.csv
```

Contains:
- image: Image identifier
- ground_truth: True label
- top_1, top_2, top_3: Model predictions
- correct: Boolean (True if ground_truth in top 3)

### 2. Visualizations

**Architecture Diagram**
```
results/architecture_20251120_HHMMSS.png
```
- System workflow visualization
- Agent connections
- Data flow

**Confusion Matrix**
```
results/confusion_matrix_20251120_HHMMSS.png
```
- 9×9 heatmap
- True vs Predicted labels
- Color-coded counts

**ROC Curves**
```
results/roc_curves_20251120_HHMMSS.png
```
- One curve per class
- AUC scores displayed
- Multi-class performance

**Accuracy Comparison**
```
results/accuracy_comparison_20251120_HHMMSS.png
```
- Top-1 vs Top-3 accuracy
- Per-category breakdown
- Sample counts

### 3. Metrics Reports

**AUC Scores**
```
results/auc_scores_20251120_HHMMSS.txt
```
- AUC for each category
- Mean AUC across all classes

**Performance Metrics**
```
results/performance_metrics_20251120_HHMMSS.txt
```
- Precision, Recall, F1-score
- Per-category breakdown
- Overall accuracy statistics

## Troubleshooting

### Issue: "Connection refused" error

**Solution**: 
1. Start LM Studio
2. Load medgemma-27b-multimodal model
3. Enable local server (Settings → Server → Start Server)
4. Verify port 1234 is accessible

### Issue: Slow processing (<1 img/s)

**Possible causes**:
- Model not fully loaded in VRAM
- CPU inference (very slow)
- System resource constraints

**Solutions**:
- Ensure GPU is being used
- Close other applications
- Check LM Studio settings for GPU acceleration

### Issue: Out of memory errors

**Solutions**:
- Reduce batch size in `batch_processor.py`
- Close other applications
- Restart LM Studio
- Use a smaller model if available

### Issue: JSON parsing errors

**Cause**: Model not following output format

**Solutions**:
- Check model temperature (should be 0.1)
- Verify correct model is loaded
- Check system prompt in `config.py`

## Performance Optimization

### For Faster Processing

1. **GPU Acceleration**: Ensure LM Studio uses GPU
2. **Batch Processing**: Already implemented
3. **Model Quantization**: Use quantized version of medgemma if available
4. **Parallel Processing**: Run multiple instances (advanced)

### For Better Accuracy

1. **Temperature**: Lower = more consistent (current: 0.1)
2. **Prompt Engineering**: Modify system prompt in `config.py`
3. **Model Selection**: Try different multimodal models
4. **Fine-tuning**: Fine-tune model on dermatology data (advanced)

## Monitoring System Resources

### Windows Task Manager

Monitor while running:
- **GPU Usage**: Should be high (80-100%)
- **RAM Usage**: Should be stable
- **CPU Usage**: Moderate (20-40%)

### LM Studio Console

Check for:
- Model load status
- Inference time per request
- Error messages

## After Completion

### 1. Review Results

```bash
# View summary
type results\performance_metrics_TIMESTAMP.txt

# Open visualizations
start results\confusion_matrix_TIMESTAMP.png
start results\roc_curves_TIMESTAMP.png
```

### 2. Analyze Performance

Key metrics to check:
- **Overall Top-3 Accuracy**: Target >85%
- **Per-class AUC**: Should be >0.7 for most classes
- **Confusion Matrix**: Identify commonly confused pairs

### 3. Generate Report

The system automatically creates comprehensive reports. Review:
- Classification report (precision/recall/F1)
- AUC scores by category
- Accuracy comparison chart

## Next Steps

After successful run:

1. **Analyze Results**: Review confusion matrix for patterns
2. **Identify Weaknesses**: Which classes have low accuracy?
3. **Improve System**: 
   - Adjust prompts for problematic classes
   - Try different models
   - Implement ensemble methods
4. **Share Results**: Use generated visualizations for presentations

## Support

If you encounter issues:

1. Check `results/results_temp.csv` for partial results
2. Review error messages in console
3. Verify LM Studio logs
4. Test with `run_sample.py` first

## Estimated Resource Requirements

- **RAM**: 16GB minimum, 32GB recommended
- **VRAM**: 8GB minimum for medgemma-27b
- **Disk Space**: 5GB for results and visualizations
- **Time**: 14-21 hours for full dataset
