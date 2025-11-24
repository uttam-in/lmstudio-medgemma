"""
Script to generate confusion matrices, AUC scores, and ROC curves
for Pneumonia, Atelectasis, and Fracture predictions.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report
import seaborn as sns
import os

# Read the results CSV
csv_path = 'results_osai/results_temp_24k.csv'
df = pd.read_csv(csv_path)

print(f"Loaded {len(df)} records from {csv_path}")
print(f"\nColumns: {df.columns.tolist()}")

# Define conditions to analyze
conditions = ['Pneumonia', 'Atelectasis', 'Fracture']

# Create output directory for plots
output_dir = 'results_osai/analysis_plots'
os.makedirs(output_dir, exist_ok=True)

# Function to convert predictions to binary
def convert_to_binary(pred_series):
    """Convert 'Present'/'Absent' to 1/0"""
    return (pred_series == 'Present').astype(int)

# Analyze each condition
for condition in conditions:
    print(f"\n{'='*60}")
    print(f"Analyzing: {condition}")
    print(f"{'='*60}")
    
    # Get column names
    pred_col = f'{condition}_predicted'
    truth_col = f'{condition}_ground_truth'
    
    # Convert predictions to binary (Present=1, Absent=0)
    y_pred = convert_to_binary(df[pred_col])
    y_true = df[truth_col].astype(int)
    
    # Calculate confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    print(f"\nConfusion Matrix:")
    print(f"True Negatives:  {tn}")
    print(f"False Positives: {fp}")
    print(f"False Negatives: {fn}")
    print(f"True Positives:  {tp}")
    
    # Calculate metrics
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"\nMetrics:")
    print(f"Accuracy:    {accuracy:.4f}")
    print(f"Precision:   {precision:.4f}")
    print(f"Recall:      {recall:.4f}")
    print(f"Specificity: {specificity:.4f}")
    print(f"F1-Score:    {f1:.4f}")
    
    # Calculate ROC curve and AUC
    fpr, tpr, thresholds = roc_curve(y_true, y_pred)
    roc_auc = auc(fpr, tpr)
    
    print(f"\nAUC Score: {roc_auc:.4f}")
    
    # Create figure with 2 subplots
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Confusion Matrix
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0],
                xticklabels=['Absent', 'Present'],
                yticklabels=['Absent', 'Present'])
    axes[0].set_title(f'{condition} - Confusion Matrix')
    axes[0].set_ylabel('True Label')
    axes[0].set_xlabel('Predicted Label')
    
    # Add metrics text
    metrics_text = f'Accuracy: {accuracy:.4f}\nPrecision: {precision:.4f}\nRecall: {recall:.4f}\nF1-Score: {f1:.4f}'
    axes[0].text(1.5, -0.3, metrics_text, fontsize=10, 
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Plot 2: ROC Curve
    axes[1].plot(fpr, tpr, color='darkorange', lw=2, 
                label=f'ROC curve (AUC = {roc_auc:.4f})')
    axes[1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
    axes[1].set_xlim([0.0, 1.0])
    axes[1].set_ylim([0.0, 1.05])
    axes[1].set_xlabel('False Positive Rate')
    axes[1].set_ylabel('True Positive Rate')
    axes[1].set_title(f'{condition} - ROC Curve')
    axes[1].legend(loc="lower right")
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    output_path = os.path.join(output_dir, f'{condition.lower()}_analysis.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: {output_path}")
    plt.close()

# Create summary comparison plot
print(f"\n{'='*60}")
print("Creating Summary Comparison")
print(f"{'='*60}")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, condition in enumerate(conditions):
    pred_col = f'{condition}_predicted'
    truth_col = f'{condition}_ground_truth'
    
    y_pred = convert_to_binary(df[pred_col])
    y_true = df[truth_col].astype(int)
    
    cm = confusion_matrix(y_true, y_pred)
    
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                xticklabels=['Absent', 'Present'],
                yticklabels=['Absent', 'Present'])
    axes[idx].set_title(f'{condition}')
    axes[idx].set_ylabel('True Label')
    axes[idx].set_xlabel('Predicted Label')

plt.suptitle('Confusion Matrices - All Conditions', fontsize=16, y=1.02)
plt.tight_layout()

summary_path = os.path.join(output_dir, 'all_conditions_comparison.png')
plt.savefig(summary_path, dpi=300, bbox_inches='tight')
print(f"\nSummary plot saved to: {summary_path}")
plt.close()

# Create summary table
print(f"\n{'='*60}")
print("Summary Table")
print(f"{'='*60}")

summary_data = []
for condition in conditions:
    pred_col = f'{condition}_predicted'
    truth_col = f'{condition}_ground_truth'
    
    y_pred = convert_to_binary(df[pred_col])
    y_true = df[truth_col].astype(int)
    
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    fpr, tpr, _ = roc_curve(y_true, y_pred)
    roc_auc = auc(fpr, tpr)
    
    summary_data.append({
        'Condition': condition,
        'Accuracy': f'{accuracy:.4f}',
        'Precision': f'{precision:.4f}',
        'Recall': f'{recall:.4f}',
        'F1-Score': f'{f1:.4f}',
        'AUC': f'{roc_auc:.4f}',
        'TP': tp,
        'TN': tn,
        'FP': fp,
        'FN': fn
    })

summary_df = pd.DataFrame(summary_data)
print("\n", summary_df.to_string(index=False))

# Save summary to CSV
summary_csv_path = os.path.join(output_dir, 'metrics_summary.csv')
summary_df.to_csv(summary_csv_path, index=False)
print(f"\nSummary saved to: {summary_csv_path}")

print(f"\n{'='*60}")
print("Analysis Complete!")
print(f"{'='*60}")
print(f"All plots saved to: {output_dir}/")
