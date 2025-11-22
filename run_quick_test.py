"""Quick test script - analyzes just 3 X-rays to verify system works."""

import os
import pandas as pd
from pathlib import Path
from datetime import datetime
from graph import create_workflow
from config import GROUND_TRUTH_CSV, RESULTS_PATH, TARGET_CONDITIONS

def quick_test():
    """Run a quick test with 3 images."""
    print("=" * 80)
    print("QUICK TEST - Analyzing 3 Chest X-Rays")
    print("=" * 80)
    
    # Load ground truth
    print("\n[1] Loading ground truth...")
    ground_truth_df = pd.read_csv(GROUND_TRUTH_CSV)
    print(f"✓ Loaded {len(ground_truth_df)} records")
    
    # Get 3 test images with different conditions
    print("\n[2] Selecting test images...")
    test_images = []
    
    # Get one with Pneumonia
    pneumonia_img = ground_truth_df[ground_truth_df['Pneumonia'] == 1.0].iloc[0]['Path']
    test_images.append(pneumonia_img)
    print(f"  - Image with Pneumonia: {Path(pneumonia_img).name}")
    
    # Get one with Atelectasis
    atelectasis_img = ground_truth_df[ground_truth_df['Atelectasis'] == 1.0].iloc[0]['Path']
    test_images.append(atelectasis_img)
    print(f"  - Image with Atelectasis: {Path(atelectasis_img).name}")
    
    # Get one with Fracture
    fracture_img = ground_truth_df[ground_truth_df['Fracture'] == 1.0].iloc[0]['Path']
    test_images.append(fracture_img)
    print(f"  - Image with Fracture: {Path(fracture_img).name}")
    
    # Create workflow
    print("\n[3] Creating workflow...")
    workflow = create_workflow(ground_truth_df)
    print("✓ Workflow ready")
    
    # Process images
    print("\n[4] Processing images...")
    print("-" * 80)
    
    results = []
    
    for idx, image_path in enumerate(test_images, 1):
        print(f"\nProcessing {idx}/3: {Path(image_path).name}")
        
        initial_state = {
            "image_path": image_path,
            "image_name": "",
            "image_data": b"",
            "prediction": {},
            "ground_truth": {},
            "evaluation": {},
            "error": ""
        }
        
        try:
            final_state = workflow.invoke(initial_state)
            
            if not final_state.get("error"):
                print(f"✓ Analysis complete")
                
                # Show results
                print(f"\n  Ground Truth:")
                for condition in TARGET_CONDITIONS:
                    gt_value = final_state["ground_truth"].get(condition, 0.0)
                    print(f"    {condition}: {'Present' if gt_value == 1.0 else 'Absent'}")
                
                print(f"\n  AI Prediction:")
                for condition in TARGET_CONDITIONS:
                    pred_value = final_state["prediction"].get(condition, "Absent")
                    correct = final_state["evaluation"].get(condition, False)
                    status = "✓" if correct else "✗"
                    print(f"    {condition}: {pred_value} {status}")
                
                # Save result
                result_row = {
                    "image_path": image_path,
                    "image_name": Path(image_path).name
                }
                
                for condition in TARGET_CONDITIONS:
                    result_row[f"{condition}_predicted"] = final_state["prediction"].get(condition, "Absent")
                    result_row[f"{condition}_ground_truth"] = final_state["ground_truth"].get(condition, 0.0)
                    result_row[f"{condition}_correct"] = final_state["evaluation"].get(condition, False)
                
                results.append(result_row)
            else:
                print(f"✗ Error: {final_state['error']}")
                
        except Exception as e:
            print(f"✗ Exception: {str(e)}")
    
    # Save results
    print("\n" + "=" * 80)
    print("[5] RESULTS")
    print("=" * 80)
    
    if results:
        df_results = pd.DataFrame(results)
        
        # Calculate accuracy
        print("\nAccuracy per condition:")
        for condition in TARGET_CONDITIONS:
            correct = df_results[f"{condition}_correct"].sum()
            total = len(df_results)
            accuracy = (correct / total * 100) if total > 0 else 0
            print(f"  {condition}: {correct}/{total} ({accuracy:.2f}%)")
        
        # Save to CSV
        os.makedirs(RESULTS_PATH, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"{RESULTS_PATH}/quick_test_{timestamp}.csv"
        df_results.to_csv(results_file, index=False)
        print(f"\n✓ Results saved to: {results_file}")
        
        print("\nFull results:")
        print(df_results.to_string(index=False))
    else:
        print("\nNo results generated.")
    
    print("\n" + "=" * 80)
    print("Quick test complete!")
    print("To process more images, run: python main.py")
    print("=" * 80)

if __name__ == "__main__":
    quick_test()
