import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.preprocessing import label_binarize
from itertools import cycle

# Read the CSV file
df = pd.read_csv('results/results_20251121_112550.csv')

print(f"Total samples: {len(df)}")
print(f"Accuracy: {df['correct'].sum() / len(df) * 100:.2f}%")
print(f"\nClass distribution:")
print(df['ground_truth'].value_counts())

# Get unique classes
classes = sorted(df['ground_truth'].unique())
n_classes = len(classes)
print(f"\nNumber of classes: {n_classes}")
print(f"Classes: {classes}")

# Create confusion matrix
y_true = df['ground_truth']
y_pred = df['top_1']
cm = confusion_matrix(y_true, y_pred, labels=classes)

# Plot confusion matrix
plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=classes, yticklabels=classes,
            cbar_kws={'label': 'Count'})
plt.title('Confusion Matrix', fontsize=16, fontweight='bold')
plt.ylabel('True Label', fontsize=12)
plt.xlabel('Predicted Label', fontsize=12)
plt.tight_layout()
plt.savefig('results/confusion_matrix.png', dpi=300, bbox_inches='tight')
print("\n✓ Confusion matrix saved to: results/confusion_matrix.png")
plt.close()

# For ROC curve, we need probability scores
# Since we only have top-k predictions, we'll create a simplified version
# We'll treat top_1 match as probability 1.0, top_2 as 0.5, top_3 as 0.25, else 0

# Create probability matrix for ROC curves
# For each sample and class, assign probability based on ranking
def create_probability_matrix(df, classes):
    n_samples = len(df)
    n_classes = len(classes)
    prob_matrix = np.zeros((n_samples, n_classes))
    
    for i, row in df.iterrows():
        for j, cls in enumerate(classes):
            if row['top_1'] == cls:
                prob_matrix[i, j] = 1.0
            elif row['top_2'] == cls:
                prob_matrix[i, j] = 0.5
            elif row['top_3'] == cls:
                prob_matrix[i, j] = 0.25
    
    return prob_matrix

# Binarize the ground truth labels
y_true_bin = label_binarize(y_true, classes=classes)
y_score = create_probability_matrix(df, classes)

# Compute ROC curve and AUC for each class
fpr = dict()
tpr = dict()
roc_auc = dict()

for i, cls in enumerate(classes):
    fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], y_score[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Compute micro-average ROC curve and AUC
fpr["micro"], tpr["micro"], _ = roc_curve(y_true_bin.ravel(), y_score.ravel())
roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

# Plot ROC curves
plt.figure(figsize=(14, 10))

# Plot micro-average ROC curve
plt.plot(fpr["micro"], tpr["micro"],
         label=f'Micro-average (AUC = {roc_auc["micro"]:.3f})',
         color='deeppink', linestyle='--', linewidth=3)

# Plot ROC curve for each class
colors = cycle(['aqua', 'darkorange', 'cornflowerblue', 'green', 'red', 
                'purple', 'brown', 'pink', 'gray', 'olive'])
for i, color, cls in zip(range(n_classes), colors, classes):
    plt.plot(fpr[i], tpr[i], color=color, lw=2,
             label=f'{cls} (AUC = {roc_auc[i]:.3f})')

# Plot diagonal line
plt.plot([0, 1], [0, 1], 'k--', lw=2, label='Random Classifier')

plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate', fontsize=12)
plt.ylabel('True Positive Rate', fontsize=12)
plt.title('ROC Curves - Multi-class Classification', fontsize=16, fontweight='bold')
plt.legend(loc="lower right", fontsize=9)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('results/roc_curves.png', dpi=300, bbox_inches='tight')
print("✓ ROC curves saved to: results/roc_curves.png")
plt.close()

# Create AUC bar chart
plt.figure(figsize=(12, 6))
auc_values = [roc_auc[i] for i in range(n_classes)]
bars = plt.bar(classes, auc_values, color='steelblue', edgecolor='black', alpha=0.7)

# Add value labels on bars
for bar, val in zip(bars, auc_values):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{val:.3f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Add micro-average line
plt.axhline(y=roc_auc["micro"], color='red', linestyle='--', linewidth=2,
            label=f'Micro-average AUC = {roc_auc["micro"]:.3f}')

plt.xlabel('Class', fontsize=12)
plt.ylabel('AUC Score', fontsize=12)
plt.title('AUC Score by Class', fontsize=16, fontweight='bold')
plt.ylim([0, 1.1])
plt.legend(fontsize=10)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('results/auc_scores.png', dpi=300, bbox_inches='tight')
print("✓ AUC scores saved to: results/auc_scores.png")
plt.close()

# Print summary statistics
print("\n" + "="*60)
print("SUMMARY STATISTICS")
print("="*60)
print(f"\nOverall Accuracy: {df['correct'].sum() / len(df) * 100:.2f}%")
print(f"Micro-average AUC: {roc_auc['micro']:.4f}")
print(f"\nPer-class AUC scores:")
for i, cls in enumerate(classes):
    print(f"  {cls:6s}: {roc_auc[i]:.4f}")

print("\n" + "="*60)
print("All visualizations saved successfully!")
print("="*60)
