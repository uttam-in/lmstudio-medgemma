"""System check script to verify all components are ready."""

import sys
import os
from pathlib import Path
import requests

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 9:
        print("  ✓ Python version OK")
        return True
    else:
        print("  ✗ Python 3.9+ required")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    required = [
        'langgraph', 'langchain', 'langchain_openai', 
        'pandas', 'matplotlib', 'seaborn', 'sklearn', 'PIL'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n  Install missing packages: pip install -r requirements.txt")
        return False
    return True

def check_lm_studio():
    """Check if LM Studio is running."""
    try:
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print("  ✓ LM Studio is running")
            if 'data' in models and len(models['data']) > 0:
                model_name = models['data'][0].get('id', 'Unknown')
                print(f"  ✓ Model loaded: {model_name}")
                return True
            else:
                print("  ⚠ No model loaded in LM Studio")
                return False
        else:
            print("  ✗ LM Studio not responding correctly")
            return False
    except requests.exceptions.RequestException as e:
        print("  ✗ Cannot connect to LM Studio")
        print(f"    Error: {e}")
        print("    Make sure LM Studio is running on http://localhost:1234")
        return False

def check_data_files():
    """Check if required data files exist."""
    archive_path = Path("archive")
    ground_truth = archive_path / "ISIC_2019_Training_GroundTruth.csv"
    
    if not archive_path.exists():
        print("  ✗ archive/ folder not found")
        return False
    
    print(f"  ✓ archive/ folder exists")
    
    if not ground_truth.exists():
        print("  ✗ Ground truth CSV not found")
        return False
    
    print(f"  ✓ Ground truth CSV exists")
    
    # Check for image folders
    categories = ['MEL', 'NV', 'BCC', 'AK', 'BKL', 'DF', 'VASC', 'SCC']
    found_categories = []
    total_images = 0
    
    for cat in categories:
        cat_path = archive_path / cat
        if cat_path.exists():
            images = list(cat_path.glob("*.jpg"))
            if images:
                found_categories.append(cat)
                total_images += len(images)
                print(f"  ✓ {cat}: {len(images)} images")
    
    if found_categories:
        print(f"\n  Total: {total_images} images across {len(found_categories)} categories")
        return True
    else:
        print("  ✗ No image folders found")
        return False

def check_graphviz():
    """Check if Graphviz is installed."""
    try:
        import graphviz
        print("  ✓ Graphviz Python package installed")
        
        # Try to create a simple graph to verify system installation
        try:
            dot = graphviz.Digraph()
            dot.node('test', 'Test')
            # This will fail if Graphviz system binaries are not installed
            dot.render('test_graphviz', format='png', cleanup=True)
            os.remove('test_graphviz.png')
            print("  ✓ Graphviz system binaries installed")
            return True
        except Exception as e:
            print("  ⚠ Graphviz Python package OK, but system binaries may be missing")
            print("    Download from: https://graphviz.org/download/")
            return True  # Not critical, just a warning
    except ImportError:
        print("  ✗ Graphviz not installed")
        print("    Install: pip install graphviz")
        return False

def main():
    """Run all system checks."""
    print("=" * 80)
    print("SYSTEM CHECK - Dermatology Classification System")
    print("=" * 80)
    
    checks = {
        "Python Version": check_python_version,
        "Python Dependencies": check_dependencies,
        "LM Studio Connection": check_lm_studio,
        "Data Files": check_data_files,
        "Graphviz": check_graphviz
    }
    
    results = {}
    
    for name, check_func in checks.items():
        print(f"\n[{name}]")
        results[name] = check_func()
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    all_passed = all(results.values())
    
    for name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:8s} - {name}")
    
    print("\n" + "=" * 80)
    
    if all_passed:
        print("✓ ALL CHECKS PASSED - System is ready!")
        print("\nNext steps:")
        print("  1. Test with sample: python run_sample.py")
        print("  2. Run full dataset: python main.py")
    else:
        print("✗ SOME CHECKS FAILED - Please fix the issues above")
        print("\nCommon fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Start LM Studio and load medgemma-27b-multimodal")
        print("  - Verify archive/ folder contains images")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
