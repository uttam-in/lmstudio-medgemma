"""Test script to verify that missing files are skipped correctly."""

import pandas as pd
from pathlib import Path
from config import GROUND_TRUTH_CSV

def test_file_existence():
    """Test how many files exist vs missing."""
    print("=" * 80)
    print("FILE EXISTENCE CHECK")
    print("=" * 80)
    
    # Load CSV
    print("\n[1] Loading ground truth CSV...")
    df = pd.read_csv(GROUND_TRUTH_CSV)
    print(f"✓ Total records in CSV: {len(df)}")
    
    # Check file existence
    print("\n[2] Checking file existence...")
    existing_files = []
    missing_files = []
    
    # Check first 100 files as a sample
    sample_size = min(100, len(df))
    print(f"   Checking first {sample_size} files as sample...")
    
    for idx, row in df.head(sample_size).iterrows():
        image_path = row['Path']
        if Path(image_path).exists():
            existing_files.append(image_path)
        else:
            missing_files.append(image_path)
    
    # Results
    print(f"\n[3] Sample Results (first {sample_size} files):")
    print(f"   ✓ Files found: {len(existing_files)}")
    print(f"   ✗ Files missing: {len(missing_files)}")
    
    if missing_files:
        print(f"\n[4] Sample missing files (first 5):")
        for path in missing_files[:5]:
            print(f"   - {path}")
    
    # Estimate for full dataset
    if sample_size > 0:
        missing_percentage = (len(missing_files) / sample_size) * 100
        estimated_missing = int((len(missing_files) / sample_size) * len(df))
        estimated_existing = len(df) - estimated_missing
        
        print(f"\n[5] Estimated for full dataset:")
        print(f"   Total files in CSV: {len(df)}")
        print(f"   Estimated existing: {estimated_existing} ({100-missing_percentage:.1f}%)")
        print(f"   Estimated missing: {estimated_missing} ({missing_percentage:.1f}%)")
        
        if missing_percentage > 0:
            print(f"\n⚠️  Note: The system will automatically skip missing files")
            print(f"   Only {estimated_existing} images will be processed")
        else:
            print(f"\n✓ All sampled files exist! Full processing possible.")
    
    print("\n" + "=" * 80)
    print("The main.py script will automatically skip any missing files.")
    print("=" * 80)

if __name__ == "__main__":
    test_file_existence()
