"""Generate visualizations for the classification results."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report
from sklearn.preprocessing import label_binarize
import graphviz
from pathlib import Path
from config import CATEGORIES, RESULTS_PATH


def generate_architecture_diagram(timestamp: str) -> str:
    """Generate system architecture diagram using Graphviz."""
    dot = graphviz.Digraph(comment='Dermatology Classification System Architecture')
    dot.attr(rankdir='TB', size='12,10')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
    
    # Define colors
    color_orchestrator = '#E8F4F8'
    color_agent = '#B8E6F0'
    color_llm = '#FF9966'
    color_io = '#FFE6CC'
    
    # Orchestrator
    dot.node('orchestrator', 'Orchestrator\n(LangGraph StateGraph)', 
             fillcolor=color_orchestrator, fontsize='14', fontname='Arial Bold')
    
    # Agents
    dot.node('input', 'Input Handler\n(Load & Preprocess)', fillcolor=color_agent)
    dot.node('processor', 'Multimodal Media\nProcessor', fillcolor=color_agent)
    dot.node('evaluator', 'Result Evaluator\n(Compare with Ground Truth)', fillcolor=color_agent)
    dot.node('output', 'Output Handler\n(Store Results)', fillcolor=color_agent)
    
    # LLM
    dot.node('llm', 'Generative AI LLM\n(medgemma-27b-multimodal)\nvia LM Studio', 
             fillcolor=color_llm, shape='box3d', fontsize='12')
    
    # I/O
    dot.node('images', 'Dermatology Images\n(archive/)', fillcolor=color_io, shape='folder')
    dot.node('ground_truth', 'Ground Truth CSV', fillcolor=color_io, shape='note')
    dot.node('results', 'Results & Metrics', fillcolor=color_io, shape='note')
    
    # Edges - Main workflow
    dot.edge('orchestrator', 'input', label='1')
    dot.edge('input', 'processor', label='2')
    dot.edge('processor', 'evaluator', label='3')
    dot.edge('evaluator', 'output', label='4')
    
    # Edges - LLM connection
    dot.edge('processor', 'llm', label='image + prompt', style='dashed', color='#FF6633')
    dot.edge('llm', 'processor', label='top-3 predictions', style='dashed', color='#FF6633')
    
    # Edges - Data flow
    dot.edge('images', 'input', style='dotted')
    dot.edge('ground_truth', 'evaluator', style='dotted')
    dot.edge('output', 'results', style='dotted')
    dot.edge('orchestrator', 'output', label='5', style='invis')
    
    # Save
    output_file = f"{RESULTS_PATH}/architecture_{timestamp}"
    dot.render(output_file, format='png', cleanup=True)
    
    return f"{output_file}.png"


def generate_confusion_matrix(df_results: pd.DataFrame, timestamp: str) -> str:
    """Generate confusion matrix heatmap."""
    # Get all categories
    all_categories = list(CATEGORIES.keys())
    
    # Prepare data
    y_true = df_results['ground_truth'].values
    y_pred = df_results['top_1'].values
    
    # Create confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=all_categories)
    
    # Plot
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=all_categories, yticklabels=all_categories,
                cbar_kws={'label': 'Count'})
    plt.title('Confusion Matrix - Dermatology Image Classification\n(Top-1 Predictions)', 
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
    plt.ylabel('True Label', fontsize=12, fontweight='bold')
    plt.tight_layout()
    
    output_file = f"{RESULTS_PATH}/confusion_matrix_{timestamp}.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_file


def generate_roc_curves(df_results: pd.DataFrame, ground_truth_df: pd.DataFrame, timestamp: str) -> str:
    """Generate ROC curves and calculate AUC for each class."""
    all_categories = [cat for cat in CATEGORIES.keys() if cat != 'UNK']
    
    # Prepare true labels (one-hot encoded)
    y_true_binary = []
    y_scores = []
    
    for _, row in df_results.iterrows():
        image_name = row['image']
        true_label = row['ground_truth']
        
        # Get true label one-hot
        true_vector = [1 if cat == true_label else 0 for cat in all_categories]
        y_true_binary.append(true_vector)
        
        # Get prediction scores (simulate probabilities based on ranking)
        pred_vector = [0.0] * len(all_categories)
        for i, cat in enumerate(all_categories):
            if cat == row['top_1']:
                pred_vector[i] = 1.0
            elif cat == row['top_2']:
                pred_vector[i] = 0.6
            elif cat == row['top_3']:
                pred_vector[i] = 0.3
        y_scores.append(pred_vector)
    
    y_true_binary = np.array(y_true_binary)
    y_scores = np.array(y_scores)
    
    # Calculate ROC curve and AUC for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    
    for i, category in enumerate(all_categories):
        fpr[i], tpr[i], _ = roc_curve(y_true_binary[:, i], y_scores[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    
    # Plot ROC curves
    plt.figure(figsize=(14, 10))
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(all_categories)))
    
    for i, (category, color) in enumerate(zip(all_categories, colors)):
        plt.plot(fpr[i], tpr[i], color=color, lw=2,
                label=f'{category} (AUC = {roc_auc[i]:.3f})')
    
    plt.plot([0, 1], [0, 1], 'k--', lw=2, label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12, fontweight='bold')
    plt.ylabel('True Positive Rate', fontsize=12, fontweight='bold')
    plt.title('ROC Curves - Multi-Class Classification\nDermatology Image Classification System', 
              fontsize=14, fontweight='bold', pad=20)
    plt.legend(loc="lower right", fontsize=10)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    output_file = f"{RESULTS_PATH}/roc_curves_{timestamp}.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save AUC scores to text file
    auc_file = f"{RESULTS_PATH}/auc_scores_{timestamp}.txt"
    with open(auc_file, 'w') as f:
        f.write("AUC Scores by Category\n")
        f.write("=" * 50 + "\n\n")
        for i, category in enumerate(all_categories):
            f.write(f"{category:6s}: {roc_auc[i]:.4f}\n")
        f.write("\n" + "=" * 50 + "\n")
        f.write(f"Mean AUC: {np.mean(list(roc_auc.values())):.4f}\n")
    
    print(f"  AUC scores saved to: {auc_file}")
    
    return output_file


def generate_performance_metrics(df_results: pd.DataFrame, timestamp: str) -> str:
    """Generate detailed performance metrics."""
    y_true = df_results['ground_truth'].values
    y_pred_top1 = df_results['top_1'].values
    
    # Classification report
    report = classification_report(y_true, y_pred_top1, 
                                   labels=list(CATEGORIES.keys()),
                                   target_names=list(CATEGORIES.keys()),
                                   zero_division=0)
    
    # Save to file
    metrics_file = f"{RESULTS_PATH}/performance_metrics_{timestamp}.txt"
    with open(metrics_file, 'w') as f:
        f.write("PERFORMANCE METRICS\n")
        f.write("=" * 80 + "\n\n")
        
        # Overall accuracy
        top1_acc = (df_results['top_1'] == df_results['ground_truth']).mean()
        top3_acc = df_results['correct'].mean()
        
        f.write(f"Top-1 Accuracy: {top1_acc:.4f} ({top1_acc*100:.2f}%)\n")
        f.write(f"Top-3 Accuracy: {top3_acc:.4f} ({top3_acc*100:.2f}%)\n")
        f.write(f"Total Images: {len(df_results)}\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("CLASSIFICATION REPORT (Top-1 Predictions)\n")
        f.write("=" * 80 + "\n\n")
        f.write(report)
        
        # Per-category breakdown
        f.write("\n" + "=" * 80 + "\n")
        f.write("PER-CATEGORY BREAKDOWN\n")
        f.write("=" * 80 + "\n\n")
        
        for category in CATEGORIES.keys():
            cat_data = df_results[df_results['ground_truth'] == category]
            if len(cat_data) > 0:
                cat_top1_acc = (cat_data['top_1'] == category).mean()
                cat_top3_acc = cat_data['correct'].mean()
                f.write(f"{category:6s} - Count: {len(cat_data):5d} | "
                       f"Top-1: {cat_top1_acc:.3f} | Top-3: {cat_top3_acc:.3f}\n")
    
    return metrics_file


def generate_accuracy_comparison(df_results: pd.DataFrame, timestamp: str) -> str:
    """Generate bar chart comparing Top-1 vs Top-3 accuracy."""
    categories = []
    top1_accuracies = []
    top3_accuracies = []
    counts = []
    
    for category in CATEGORIES.keys():
        cat_data = df_results[df_results['ground_truth'] == category]
        if len(cat_data) > 0:
            categories.append(category)
            counts.append(len(cat_data))
            top1_accuracies.append((cat_data['top_1'] == category).mean() * 100)
            top3_accuracies.append(cat_data['correct'].mean() * 100)
    
    # Plot
    x = np.arange(len(categories))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(14, 8))
    bars1 = ax.bar(x - width/2, top1_accuracies, width, label='Top-1 Accuracy', 
                   color='#3498db', alpha=0.8)
    bars2 = ax.bar(x + width/2, top3_accuracies, width, label='Top-3 Accuracy', 
                   color='#2ecc71', alpha=0.8)
    
    ax.set_xlabel('Category', fontsize=12, fontweight='bold')
    ax.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
    ax.set_title('Classification Accuracy by Category\nTop-1 vs Top-3 Predictions', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
    
    # Add sample counts
    for i, (cat, count) in enumerate(zip(categories, counts)):
        ax.text(i, -8, f'n={count}', ha='center', fontsize=9, style='italic')
    
    plt.tight_layout()
    
    output_file = f"{RESULTS_PATH}/accuracy_comparison_{timestamp}.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_file


def generate_all_visualizations(df_results: pd.DataFrame, ground_truth_df: pd.DataFrame, 
                                timestamp: str) -> list:
    """Generate all visualizations and return list of file paths."""
    viz_files = []
    
    print("  Generating architecture diagram...")
    viz_files.append(generate_architecture_diagram(timestamp))
    
    print("  Generating confusion matrix...")
    viz_files.append(generate_confusion_matrix(df_results, timestamp))
    
    print("  Generating ROC curves and AUC scores...")
    viz_files.append(generate_roc_curves(df_results, ground_truth_df, timestamp))
    
    print("  Generating performance metrics...")
    viz_files.append(generate_performance_metrics(df_results, timestamp))
    
    print("  Generating accuracy comparison chart...")
    viz_files.append(generate_accuracy_comparison(df_results, timestamp))
    
    return viz_files
