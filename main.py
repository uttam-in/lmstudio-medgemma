"""Main orchestrator for the dermatology classification system."""

import os
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from graph import create_workflow
from config import ARCHIVE_PATH, GROUND_TRUTH_CSV, RESULTS_PATH, CATEGORIES
from visualizations import generate_all_visualizations
from batch_processor import BatchProcessor


def get_image_files(archive_path: str, limit: int = None):
    """Get all image files from archive folders."""
    image_files = []
    for category in CATEGORIES.keys():
        if category == "UNK":
            continue
        category_path = Path(archive_path) / category
        if category_path.exists():
            images = list(category_path.glob("*.jpg"))
            image_files.extend(images)
    
    print(f"  Total images found: {len(image_files)}")
    
    if limit:
        image_files = image_files[:limit]
        print(f"  Limited to: {limit} images")
    
    return image_files


def main():
    """Main orchestrator function."""
    print("=" * 80)
    print("DERMATOLOGY IMAGE CLASSIFICATION SYSTEM")
    print("Using LangGraph + Google Gemini API (gemini-2.0-flash-exp)")
    print("=" * 80)
    
    # Load ground truth
    print("\n[1] Loading ground truth data...")
    ground_truth_df = pd.read_csv(GROUND_TRUTH_CSV)
    print(f"✓ Loaded {len(ground_truth_df)} ground truth records")
    
    # Create workflow
    print("\n[2] Creating LangGraph workflow...")
    workflow = create_workflow(ground_truth_df)
    print("✓ Workflow created with nodes: Input Handler → Processor → Evaluator → Output Handler")
    
    # Get images to process
    print("\n[3] Scanning archive for images...")
    image_files = get_image_files(ARCHIVE_PATH, limit=None)  # Process all images
    print(f"✓ Processing {len(image_files)} images")
    
    # Process images with batch processor
    print("\n[4] Processing images...")
    print("-" * 80)
    
    batch_processor = BatchProcessor(batch_size=50, save_interval=100)
    batch_processor.start()
    
    results = []
    correct_count = 0
    
    for idx, image_path in enumerate(image_files, 1):
        # Create initial state
        initial_state = {
            "image_path": str(image_path),
            "image_name": "",
            "image_data": b"",
            "prediction": {},
            "ground_truth": "",
            "is_correct": False,
            "error": ""
        }
        
        # Run workflow
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
                
                # Update progress
                batch_processor.update_progress(idx, len(image_files), 
                                               final_state["image_name"], 
                                               final_state["is_correct"])
            else:
                batch_processor.error_count += 1
                batch_processor.update_progress(idx, len(image_files), 
                                               image_path.name, False)
                
            # Save intermediate results every save_interval
            if idx % batch_processor.save_interval == 0 and results:
                os.makedirs(RESULTS_PATH, exist_ok=True)
                temp_file = f"{RESULTS_PATH}/results_temp.csv"
                pd.DataFrame(results).to_csv(temp_file, index=False)
                
        except Exception as e:
            batch_processor.error_count += 1
            batch_processor.update_progress(idx, len(image_files), image_path.name, False)
    
    batch_processor.finish(len(image_files))
    
    # Save results
    print("\n" + "=" * 80)
    print("[5] RESULTS SUMMARY")
    print("=" * 80)
    
    if results:
        accuracy = (correct_count / len(results)) * 100
        print(f"\nTotal images processed: {len(results)}")
        print(f"Correct predictions: {correct_count}")
        print(f"Accuracy: {accuracy:.2f}%")
        
        # Save to CSV
        os.makedirs(RESULTS_PATH, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"{RESULTS_PATH}/results_{timestamp}.csv"
        
        df_results = pd.DataFrame(results)
        df_results.to_csv(results_file, index=False)
        print(f"\n✓ Results saved to: {results_file}")
        
        # Show sample results
        print("\nSample results:")
        print(df_results.head(10).to_string(index=False))
        
        # Generate visualizations
        print("\n[6] Generating visualizations...")
        print("-" * 80)
        viz_files = generate_all_visualizations(df_results, ground_truth_df, timestamp)
        print("\n✓ Visualizations generated:")
        for viz_file in viz_files:
            print(f"  - {viz_file}")
    else:
        print("\nNo results to display.")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
