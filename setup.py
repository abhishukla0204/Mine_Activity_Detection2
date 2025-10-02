"""
Installation and Setup Script for Mining Activity Monitoring Tool
Run this first to set up your environment
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def run_command(command, description):
    """Run a command and show result"""
    print(f"\n→ {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print("  ✓ Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Failed: {e}")
        return False


def main():
    print_header("Mining Activity Monitoring Tool - Setup")
    
    print("\nThis script will help you set up the tool.")
    print("\nWhat it does:")
    print("  1. Check Python version")
    print("  2. Install required packages")
    print("  3. Verify installations")
    print("  4. Create output directories")
    print("  5. Run a quick test")
    
    # Check Python version
    print_header("Step 1: Checking Python Version")
    py_version = sys.version_info
    print(f"\nPython version: {py_version.major}.{py_version.minor}.{py_version.micro}")
    
    if py_version.major == 3 and py_version.minor >= 8:
        print("✓ Python version is compatible (3.8+)")
    else:
        print("⚠️  Warning: Python 3.8 or higher is recommended")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Install requirements
    print_header("Step 2: Installing Required Packages")
    print("\nThis may take a few minutes...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    if requirements_file.exists():
        success = run_command(
            f'"{sys.executable}" -m pip install -r "{requirements_file}"',
            "Installing packages from requirements.txt"
        )
        if not success:
            print("\n⚠️  Some packages failed to install.")
            print("You may need to install them manually.")
    else:
        print("⚠️  requirements.txt not found!")
    
    # Check dependencies
    print_header("Step 3: Verifying Installations")
    
    check_script = Path(__file__).parent / "check_dependencies.py"
    if check_script.exists():
        run_command(
            f'"{sys.executable}" "{check_script}"',
            "Checking installed packages"
        )
    
    # Create output directories
    print_header("Step 4: Creating Output Directories")
    
    output_dirs = [
        Path("outputs"),
        Path("outputs/reports"),
        Path("outputs/visualizations")
    ]
    
    for dir_path in output_dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created: {dir_path}")
    
    # Check data
    print_header("Step 5: Checking Data Files")
    
    data_dir = Path("data/Singrauli")
    required_files = [
        "Singrauli_Sentinel2_RGB.tif",
        "Singrauli_SRTM_DEM.tif",
        "mine_shape/_annotations.coco.json"
    ]
    
    all_present = True
    for file_name in required_files:
        file_path = data_dir / file_name
        if file_path.exists():
            print(f"  ✓ Found: {file_name}")
        else:
            print(f"  ✗ Missing: {file_name}")
            all_present = False
    
    if not all_present:
        print("\n⚠️  Some data files are missing!")
        print("Make sure your data is in the data/Singrauli/ directory")
    
    # Final instructions
    print_header("Setup Complete!")
    
    if all_present:
        print("\n✅ Everything is ready!")
        print("\nNext steps:")
        print("  1. Run the tool:")
        print("     python main.py --data-dir data/Singrauli")
        print("\n  2. Or run the example:")
        print("     python example.py")
        print("\n  3. View results in:")
        print("     outputs/reports/")
        print("     outputs/visualizations/")
    else:
        print("\n⚠️  Setup completed with warnings")
        print("\nPlease:")
        print("  1. Check that all data files are present")
        print("  2. Verify all packages installed correctly")
        print("  3. Read START_HERE.md for instructions")
    
    print("\n📖 Documentation:")
    print("  - START_HERE.md    - Begin here!")
    print("  - QUICKSTART.md    - Quick start guide")
    print("  - README.md        - Full documentation")
    print("  - PROJECT_SUMMARY.md - Technical details")
    
    print("\n" + "=" * 60)
    print("  Thank you for using Mining Activity Monitoring Tool!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
