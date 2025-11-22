"""Check if LM Studio is running and accessible."""

import requests
from config import LMSTUDIO_BASE_URL, MODEL_NAME

def check_lmstudio():
    """Check LM Studio connection."""
    print("=" * 80)
    print("LM STUDIO CONNECTION TEST")
    print("=" * 80)
    
    print(f"\nBase URL: {LMSTUDIO_BASE_URL}")
    print(f"Model: {MODEL_NAME}")
    
    print("\n[1] Testing connection...")
    try:
        response = requests.get(f"{LMSTUDIO_BASE_URL}/models", timeout=5)
        if response.status_code == 200:
            print("✓ LM Studio is running and accessible")
            
            models = response.json()
            if models.get('data'):
                print(f"\n[2] Available models:")
                for model in models['data']:
                    model_id = model.get('id', 'unknown')
                    print(f"  - {model_id}")
                    if MODEL_NAME in model_id:
                        print(f"    ✓ Target model found!")
            else:
                print("\n⚠ No models loaded in LM Studio")
                print("  Please load the medgemma-27b-multimodal model")
        else:
            print(f"✗ Unexpected response: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to LM Studio")
        print("\nTroubleshooting:")
        print("  1. Make sure LM Studio is running")
        print("  2. Check that the server is started (green play button)")
        print("  3. Verify the port is 1234 (default)")
        print("  4. Load the medgemma-27b-multimodal model")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    check_lmstudio()
