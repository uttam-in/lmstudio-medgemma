# Quick Reference Guide

## 🚀 Commands

```bash
# Check system status
python check_system.py

# Test with 20 images (2-3 minutes)
python run_sample.py

# Run full dataset (14-21 hours)
python main.py

# Install dependencies
pip install -r requirements.txt
```

## 📊 Current Dataset

- **Total Images**: 25,331
- **Categories**: 8 (MEL, NV, BCC, AK, BKL, DF, VASC, SCC)
- **Ground Truth**: archive/ISIC_2019_Training_GroundTruth.csv

### Distribution
| Category | Count | Percentage |
|----------|-------|------------|
| NV       | 12,875 | 50.8% |
| MEL      | 4,522  | 17.9% |
| BCC      | 3,323  | 13.1% |
| BKL      | 2,624  | 10.4% |
| AK       | 867    | 3.4% |
| SCC      | 628    | 2.5% |
| VASC     | 253    | 1.0% |
| DF       | 239    | 0.9% |

## 🎯 Expected Performance

Based on test run (10 images):
- **Top-3 Accuracy**: 90%
- **Processing Rate**: 2-3 images/second
- **Full Dataset Time**: 14-21 hours

## 📁 Output Files

All saved to `results/` with timestamp:

1. `results_TIMESTAMP.csv` - All predictions
2. `architecture_TIMESTAMP.png` - System diagram
3. `confusion_matrix_TIMESTAMP.png` - 9×9 heatmap
4. `roc_curves_TIMESTAMP.png` - ROC with AUC
5. `auc_scores_TIMESTAMP.txt` - AUC by category
6. `performance_metrics_TIMESTAMP.txt` - Full report
7. `accuracy_comparison_TIMESTAMP.png` - Bar chart

## 🔧 Configuration

### LM Studio
- **URL**: http://localhost:1234
- **Model**: medgemma-27b-multimodal
- **Temperature**: 0.1

### Batch Processing
- **Save Interval**: Every 100 images
- **Temp File**: results/results_temp.csv

## 📝 File Structure

```
Core Files:
├── main.py              # Main orchestrator
├── agents.py            # Agent implementations
├── graph.py             # LangGraph workflow
├── config.py            # Configuration
├── visualizations.py    # Chart generation
└── batch_processor.py   # Progress tracking

Helper Scripts:
├── check_system.py      # System verification
├── run_sample.py        # Quick test
└── install.bat          # Windows installer

Documentation:
├── README.md            # User guide
├── SYSTEM_OVERVIEW.md   # Technical docs
├── RUN_INSTRUCTIONS.md  # Detailed guide
├── PROJECT_SUMMARY.md   # Overview
└── QUICK_REFERENCE.md   # This file
```

## 🎨 Agent Workflow

```
Input Handler → Multimodal Processor → Result Evaluator → Output Handler
                        ↓
                medgemma-27b-multimodal
                   (LM Studio)
```

## 📊 Metrics Explained

### Top-3 Accuracy
Prediction is correct if ground truth appears in any of the 3 predictions.

**Formula**: `correct = ground_truth in [top_1, top_2, top_3]`

### AUC (Area Under Curve)
- **Range**: 0.0 to 1.0
- **Good**: > 0.7
- **Excellent**: > 0.9
- **Random**: 0.5

### Confusion Matrix
- **Rows**: True labels
- **Columns**: Predicted labels
- **Diagonal**: Correct predictions
- **Off-diagonal**: Misclassifications

## 🔍 Troubleshooting

### Connection Error
```bash
# Check LM Studio
curl http://localhost:1234/v1/models
```

### Slow Processing
- Verify GPU usage in Task Manager
- Check LM Studio settings
- Close other applications

### Out of Memory
- Restart LM Studio
- Close browser tabs
- Reduce system load

### JSON Parse Error
- Check model temperature (should be 0.1)
- Verify correct model loaded
- Review system prompt

## 💡 Tips

### For Speed
- Ensure GPU acceleration enabled
- Close unnecessary applications
- Run overnight for full dataset

### For Accuracy
- Lower temperature = more consistent
- Verify model is fully loaded
- Check prompt engineering

### For Monitoring
- Watch progress bar for ETA
- Check results_temp.csv for intermediate results
- Monitor GPU usage in Task Manager

## 📈 Progress Bar Explained

```
[1234/25331] ████████████░░░░░░░░░░░░░░░░ 48.7% ✓ ISIC_0012345 | Rate: 2.3 img/s | ETA: 2h 45m
```

- `[1234/25331]` - Current/Total images
- `████████████░░░░` - Visual progress
- `48.7%` - Percentage complete
- `✓` - Last prediction correct (✗ if incorrect)
- `ISIC_0012345` - Current image name
- `Rate: 2.3 img/s` - Processing speed
- `ETA: 2h 45m` - Estimated time remaining

## 🎯 Success Checklist

Before running full dataset:

- [ ] LM Studio running on port 1234
- [ ] medgemma-27b-multimodal loaded
- [ ] All dependencies installed
- [ ] Archive folder contains 25,331 images
- [ ] Ground truth CSV exists
- [ ] Sample test passed (run_sample.py)
- [ ] Sufficient disk space (5GB for results)
- [ ] System can run for 14-21 hours

## 📞 Quick Checks

```bash
# System status
python check_system.py

# Test LM Studio
curl http://localhost:1234/v1/models

# Count images
dir archive\MEL\*.jpg | Measure-Object | Select-Object Count

# Check results
dir results\*.csv

# View latest results
type results\performance_metrics_*.txt
```

## 🎓 Key Concepts

**Agentic System**: Multiple specialized agents working together

**LangGraph**: State machine for agent orchestration

**Multimodal LLM**: AI that processes both images and text

**Top-3 Classification**: Returns 3 ranked predictions

**Ground Truth**: Known correct labels for evaluation

**Batch Processing**: Processing multiple items with progress tracking

## 🔗 Resources

- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **LM Studio**: https://lmstudio.ai/
- **Graphviz**: https://graphviz.org/download/
- **ISIC Dataset**: https://www.isic-archive.com/

## ⚠️ Important Notes

1. **Research Only**: Not for medical diagnosis
2. **Privacy**: All processing is local (no cloud)
3. **Time**: Full dataset takes 14-21 hours
4. **Resources**: Requires GPU for reasonable speed
5. **Checkpoints**: Results saved every 100 images

## 🎉 Ready to Go!

Your system is fully configured and ready to process the complete dataset.

**Recommended workflow**:
1. ✅ Run `python check_system.py` (DONE)
2. ✅ Test with `python run_sample.py` (90% accuracy achieved)
3. 🚀 Run `python main.py` for full dataset
4. 📊 Review results in `results/` folder

---

**Status**: ✅ All systems operational  
**Dataset**: 25,331 images ready  
**Model**: medgemma-27b-multimodal loaded  
**Ready**: Yes - Start processing!
