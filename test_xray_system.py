"""Test script for chest X-ray classification system."""

import pandas as pd
from pathlib import Path
from config import GROUND_TRUTH_CSV, TARGET_CONDITIONS

def test_setup():
    """Test that the system is properly configured."""
    print("=" * 80)
    print("CHEST X-RAY SYSTEM CONFIGURATION TEST")
    print("=" * 80)
    
    # Test 1: Check ground truth CSV
    print("\n[1] Testing ground truth CSV...")
    try:
        df = pd.read_csv(GROUND_TRUTH_CSV)
        print(f"✓ CSV loaded successfully")
        print(f"  - Total records: {len(df)}")
        print(f"  - Columns: {', '.join(df.columns.tolist())}")
        
        # Check target conditions exist
        print(f"\n[2] Checking target conditions...")
        for condition in TARGET_CONDITIONS:
            if condition in df.columns:
                count = df[condition].sum()
                print(f"✓ {condition}: {int(count)} positive cases")
            else:
                print(f"✗ {condition}: NOT FOUND in CSV")
        
        # Check image paths
        print(f"\n[3] Checking image paths...")
        sample_path = df['Path'].iloc[0]
        print(f"  Sample path: {sample_path}")
        
        if Path(sample_path).exists():
            print(f"✓ Sample image exists")
        else:
            print(f"✗ Sample image NOT FOUND")
            print(f"  Please ensure CheXpert images are in the correct location")
        
        # Show sample data
        print(f"\n[4] Sample data:")
        print(df[['Path'] + TARGET_CONDITIONS].head(5).to_string(index=False))
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    test_setup()
