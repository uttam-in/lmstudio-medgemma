"""Main orchestrator for the chest X-ray classification system."""

import os
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from graph import create_workflow
from config import CHEXPERT_PATH, GROUND_TRUTH_CSV, RESULTS_PATH, TARGET_CONDITIONS
from batch_processor import BatchProcessor


def get_image_files_from_csv(csv_path: str, limit: int = None):
    """Get image files from the ground truth CSV."""
    df = pd.read_csv(csv_path)
    image_paths = df['Path'].tolist()
    
    print(f"  Total images in CSV: {len(image_paths)}")
    
    if limit:
        image_paths = image_paths[:limit]
        print(f"  Limited to: {limit} images")
    
    return image_paths


def main():
    """Main orchestrator function."""
    print("=" * 80)
    print("CHEST X-RAY CLASSIFICATION SYSTEM")
    print("Using LangGraph + LM Studio (medgemma-27b-multimodal)")
    print(f"Target Conditions: {', '.join(TARGET_CONDITIONS)}")
    print("=" * 80)
    
    # Load ground truth
    print("\n[1] Loading ground truth data...")
    ground_truth_df = pd.read_csv(GROUND_TRUTH_CSV)
    print(f"✓ Loaded {len(ground_truth_df)} ground truth records")
    print(f"✓ Columns: {', '.join(ground_truth_df.columns.tolist())}")
    
    # Create workflow
    print("\n[2] Creating LangGraph workflow...")
    workflow = create_workflow(ground_truth_df)
    print("✓ Workflow created with nodes: Input Handler → Processor → Evaluator → Output Handler")
    
    # Get images to process
    print("\n[3] Loading ALL images from CSV...")
    image_paths = get_image_files_from_csv(GROUND_TRUTH_CSV, limit=None)  # Process ALL images
    print(f"✓ Processing {len(image_paths)} images")
    print(f"⚠ This will take approximately {len(image_paths) * 7 / 3600:.1f} hours")
    print(f"⚠ Results will be saved every 100 images to prevent data loss")
    
    # Process images with batch processor
    print("\n[4] Processing images...")
    print("-" * 80)
    
    batch_processor = BatchProcessor(batch_size=100, save_interval=100)
    batch_processor.start()
    
    results = []
    condition_stats = {condition: {"correct": 0, "total": 0} for condition in TARGET_CONDITIONS}
    skipped_count = 0
    
    start_time = datetime.now()
    print(f"\n⏱ Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Progress will be displayed every 10 images")
    print(f"💾 Results will be saved every 100 images")
    print(f"⚠ Files not found will be skipped automatically")
    print()
    
    for idx, image_path in enumerate(image_paths, 1):
        # Check if file exists before processing
        if not Path(image_path).exists():
            skipped_count += 1
            if skipped_count <= 10:  # Only show first 10 skipped files
                print(f"⚠ Skipping (file not found): {image_path}")
            elif skipped_count == 11:
                print(f"⚠ More files not found... (will continue silently)")
            continue
        
        # Create initial state
        initial_state = {
            "image_path": image_path,
            "image_name": "",
            "image_data": b"",
            "prediction": {},
            "ground_truth": {},
            "evaluation": {},
            "error": ""
        }
        
        # Run workflow
        try:
            final_state = workflow.invoke(initial_state)
            
            if not final_state.get("error"):
                result_row = {
                    "image_path": image_path,
                    "image_name": Path(image_path).name
                }
                
                # Add predictions and ground truth for each condition
                for condition in TARGET_CONDITIONS:
                    result_row[f"{condition}_predicted"] = final_state["prediction"].get(condition, "Absent")
                    result_row[f"{condition}_ground_truth"] = final_state["ground_truth"].get(condition, 0.0)
                    result_row[f"{condition}_correct"] = final_state["evaluation"].get(condition, False)
                    
                    # Update stats
                    condition_stats[condition]["total"] += 1
                    if final_state["evaluation"].get(condition, False):
                        condition_stats[condition]["correct"] += 1
                
                results.append(result_row)
                
                # Update progress
                batch_processor.update_progress(idx, len(image_paths), 
                                               Path(image_path).name, 
                                               all(final_state["evaluation"].values()))
            else:
                batch_processor.error_count += 1
                print(f"  Error: {final_state['error']}")
                batch_processor.update_progress(idx, len(image_paths), 
                                               Path(image_path).name, False)
                
            # Save intermediate results every save_interval
            if idx % batch_processor.save_interval == 0 and results:
                os.makedirs(RESULTS_PATH, exist_ok=True)
                temp_file = f"{RESULTS_PATH}/results_temp.csv"
                pd.DataFrame(results).to_csv(temp_file, index=False)
                print(f"\n💾 Intermediate results saved ({len(results)} images processed)")
                print(f"⏱ Current time: {datetime.now().strftime('%H:%M:%S')}")
                
                # Show current accuracy
                print("📊 Current accuracy:")
                for condition in TARGET_CONDITIONS:
                    total = condition_stats[condition]["total"]
                    correct = condition_stats[condition]["correct"]
                    accuracy = (correct / total * 100) if total > 0 else 0
                    print(f"   {condition}: {correct}/{total} ({accuracy:.2f}%)")
                print()
                
        except Exception as e:
            batch_processor.error_count += 1
            print(f"  Exception: {str(e)}")
            batch_processor.update_progress(idx, len(image_paths), Path(image_path).name, False)
    
    batch_processor.finish(len(image_paths))
    
    # Save results
    print("\n" + "=" * 80)
    print("[5] RESULTS SUMMARY")
    print("=" * 80)
    
    if results:
        end_time = datetime.now()
        duration = end_time - start_time
        hours = duration.total_seconds() / 3600
        
        # Calculate accuracy per condition
        print(f"\nTotal images in CSV: {len(image_paths)}")
        print(f"Images processed: {len(results)}")
        print(f"Images skipped (not found): {skipped_count}")
        print(f"⏱ Total processing time: {hours:.2f} hours ({duration.total_seconds()/60:.1f} minutes)")
        print(f"⚡ Average time per image: {duration.total_seconds()/len(results):.2f} seconds")
        
        print("\n📊 Final Accuracy per condition:")
        for condition in TARGET_CONDITIONS:
            total = condition_stats[condition]["total"]
            correct = condition_stats[condition]["correct"]
            accuracy = (correct / total * 100) if total > 0 else 0
            print(f"  {condition}: {correct}/{total} ({accuracy:.2f}%)")
        
        # Save to CSV
        os.makedirs(RESULTS_PATH, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"{RESULTS_PATH}/chexpert_results_{timestamp}.csv"
        
        df_results = pd.DataFrame(results)
        df_results.to_csv(results_file, index=False)
        print(f"\n✓ Results saved to: {results_file}")
        
        # Show sample results
        print("\nSample results (first 5):")
        print(df_results.head(5).to_string(index=False))
        
        print("\nSample results (last 5):")
        print(df_results.tail(5).to_string(index=False))
    else:
        print("\nNo results to display.")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
