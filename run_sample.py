"""Run a sample test with limited images to verify setup."""

import os
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from graph import create_workflow
from config import ARCHIVE_PATH, GROUND_TRUTH_CSV, RESULTS_PATH, CATEGORIES


def main():
    """Run sample test with 20 images."""
    print("=" * 80)
    print("SAMPLE TEST - Dermatology Image Classification")
    print("Testing with 20 images to verify system setup")
    print("=" * 80)
    
    # Load ground truth
    print("\n[1] Loading ground truth data...")
    ground_truth_df = pd.read_csv(GROUND_TRUTH_CSV)
    print(f"✓ Loaded {len(ground_truth_df)} ground truth records")
    
    # Create workflow
    print("\n[2] Creating LangGraph workflow...")
    workflow = create_workflow(ground_truth_df)
    print("✓ Workflow created")
    
    # Get sample images
    print("\n[3] Getting sample images...")
    image_files = []
    for category in ['MEL', 'NV', 'BCC']:
        category_path = Path(ARCHIVE_PATH) / category
        if category_path.exists():
            images = list(category_path.glob("*.jpg"))[:7]
            image_files.extend(images)
    
    print(f"✓ Selected {len(image_files)} sample images")
    
    # Process images
    print("\n[4] Processing images...")
    print("-" * 80)
    
    results = []
    correct_count = 0
    
    for idx, image_path in enumerate(image_files, 1):
        print(f"\n[{idx}/{len(image_files)}] {image_path.name}")
        
        initial_state = {
            "image_path": str(image_path),
            "image_name": "",
            "image_data": b"",
            "prediction": {},
            "ground_truth": "",
            "is_correct": False,
            "error": ""
        }
        
        try:
            final_state = workflow.invoke(initial_state)
            
            if not final_state.get("error"):
                results.append({
                    "image": final_state["image_name"],
                    "ground_truth": final_state["ground_truth"],
                    "top_1": final_state["prediction"].get("top_1"),
                    "top_2": final_state["prediction"].get("top_2"),
                    "top_3": final_state["prediction"].get("top_3"),
                    "correct": final_state["is_correct"]
                })
                
                if final_state["is_correct"]:
                    correct_count += 1
                
                status = "✓" if final_state["is_correct"] else "✗"
                print(f"  {status} GT: {final_state['ground_truth']} | "
                      f"Pred: {final_state['prediction']}")
            else:
                print(f"  Error: {final_state['error']}")
                
        except Exception as e:
            print(f"  Workflow error: {e}")
    
    # Results
    print("\n" + "=" * 80)
    print("SAMPLE TEST RESULTS")
    print("=" * 80)
    
    if results:
        accuracy = (correct_count / len(results)) * 100
        print(f"\nTotal images: {len(results)}")
        print(f"Correct: {correct_count}")
        print(f"Accuracy: {accuracy:.2f}%")
        
        print("\nResults:")
        df_results = pd.DataFrame(results)
        print(df_results.to_string(index=False))
        
        print("\n✓ Sample test complete! System is working correctly.")
        print("  Run 'python main.py' to process the full dataset.")
    else:
        print("\n✗ No results. Please check:")
        print("  1. LM Studio is running on http://localhost:1234")
        print("  2. medgemma-27b-multimodal model is loaded")
        print("  3. Archive folder contains images")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
