"""Helper script to easily adjust the number of images to process."""

import sys

def show_options():
    """Display processing options."""
    print("=" * 80)
    print("SET PROCESSING LIMIT")
    print("=" * 80)
    print("\nChoose how many images to process:\n")
    print("  1. Quick Test      - 100 images    (~12 minutes)")
    print("  2. Small Test      - 1,000 images  (~2 hours)")
    print("  3. Medium Test     - 10,000 images (~20 hours)")
    print("  4. Large Test      - 50,000 images (~4 days)")
    print("  5. Full Analysis   - ALL 223,414 images (~18 days)")
    print("  6. Custom          - Enter your own number")
    print("\n  0. Exit")
    print("=" * 80)

def update_main_py(limit_value):
    """Update main.py with the new limit."""
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find and replace the limit line
    import re
    pattern = r'image_paths = get_image_files_from_csv\(GROUND_TRUTH_CSV, limit=.*?\)'
    
    if limit_value is None:
        replacement = 'image_paths = get_image_files_from_csv(GROUND_TRUTH_CSV, limit=None)  # Process ALL images'
    else:
        replacement = f'image_paths = get_image_files_from_csv(GROUND_TRUTH_CSV, limit={limit_value})'
    
    new_content = re.sub(pattern, replacement, content)
    
    with open('main.py', 'w') as f:
        f.write(new_content)
    
    print(f"\n✓ Updated main.py to process {limit_value if limit_value else 'ALL'} images")

def main():
    """Main function."""
    show_options()
    
    try:
        choice = input("\nEnter your choice (0-6): ").strip()
        
        if choice == '0':
            print("Exiting...")
            return
        elif choice == '1':
            limit = 100
            time_est = "~12 minutes"
        elif choice == '2':
            limit = 1000
            time_est = "~2 hours"
        elif choice == '3':
            limit = 10000
            time_est = "~20 hours"
        elif choice == '4':
            limit = 50000
            time_est = "~4 days"
        elif choice == '5':
            limit = None
            time_est = "~18 days"
        elif choice == '6':
            custom = input("Enter number of images: ").strip()
            try:
                limit = int(custom)
                time_est = f"~{limit * 7 / 3600:.1f} hours"
            except ValueError:
                print("Invalid number!")
                return
        else:
            print("Invalid choice!")
            return
        
        # Confirm
        print(f"\n⚠️  You selected: {limit if limit else 'ALL 223,414'} images")
        print(f"⏱  Estimated time: {time_est}")
        confirm = input("\nProceed? (y/n): ").strip().lower()
        
        if confirm == 'y':
            update_main_py(limit)
            print("\n" + "=" * 80)
            print("✓ Configuration updated!")
            print("\nNext steps:")
            print("  1. Verify LM Studio is running: python check_lmstudio.py")
            print("  2. Run the analysis: python main.py")
            print("=" * 80)
        else:
            print("Cancelled.")
    
    except KeyboardInterrupt:
        print("\n\nCancelled.")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
