"""
Check if all required dependencies are installed
"""

import sys
import importlib

REQUIRED_PACKAGES = {
    'rasterio': 'rasterio',
    'geopandas': 'geopandas',
    'shapely': 'shapely',
    'pyproj': 'pyproj',
    'fiona': 'fiona',
    'cv2': 'opencv-python',
    'skimage': 'scikit-image',
    'numpy': 'numpy',
    'scipy': 'scipy',
    'PIL': 'pillow',
    'pandas': 'pandas',
    'matplotlib': 'matplotlib',
    'seaborn': 'seaborn',
    'folium': 'folium',
    'plotly': 'plotly',
    'yaml': 'pyyaml',
}

OPTIONAL_PACKAGES = {
    'pyvista': 'pyvista',
    'pyvistaqt': 'pyvistaqt',
}


def check_package(package_name, install_name):
    """Check if a package is installed"""
    try:
        importlib.import_module(package_name)
        return True, None
    except ImportError as e:
        return False, str(e)


def main():
    print("=" * 60)
    print("Mining Activity Monitoring Tool - Dependency Check")
    print("=" * 60)
    
    # Check required packages
    print("\n📦 Checking Required Packages...")
    print("-" * 60)
    
    missing_required = []
    for package, install_name in REQUIRED_PACKAGES.items():
        installed, error = check_package(package, install_name)
        status = "✓" if installed else "✗"
        color = "32" if installed else "31"  # Green or Red
        
        print(f"  [{status}] {install_name:20s} ", end="")
        if installed:
            print(f"\033[{color}mInstalled\033[0m")
        else:
            print(f"\033[{color}mMissing\033[0m")
            missing_required.append(install_name)
    
    # Check optional packages
    print("\n📦 Checking Optional Packages...")
    print("-" * 60)
    
    missing_optional = []
    for package, install_name in OPTIONAL_PACKAGES.items():
        installed, error = check_package(package, install_name)
        status = "✓" if installed else "○"
        color = "32" if installed else "33"  # Green or Yellow
        
        print(f"  [{status}] {install_name:20s} ", end="")
        if installed:
            print(f"\033[{color}mInstalled\033[0m")
        else:
            print(f"\033[{color}mNot Installed (optional)\033[0m")
            missing_optional.append(install_name)
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    if not missing_required:
        print("\n✅ All required packages are installed!")
        print("   You can run the tool with: python main.py --data-dir data/Singrauli")
    else:
        print(f"\n❌ {len(missing_required)} required package(s) missing:")
        for package in missing_required:
            print(f"   - {package}")
        print("\n   Install with:")
        print(f"   pip install {' '.join(missing_required)}")
        print("\n   Or install all:")
        print("   pip install -r requirements.txt")
    
    if missing_optional:
        print(f"\n⚠️  {len(missing_optional)} optional package(s) not installed:")
        for package in missing_optional:
            print(f"   - {package}")
        print("\n   These are optional but enable additional features:")
        print("   - pyvista: Advanced 3D visualizations")
        print("   - pyvistaqt: PyVista Qt backend")
        print("\n   Install with:")
        print(f"   pip install {' '.join(missing_optional)}")
    
    # Python version check
    print(f"\n🐍 Python Version: {sys.version.split()[0]}")
    py_version = sys.version_info
    if py_version.major == 3 and py_version.minor >= 8:
        print("   ✓ Python version is compatible (3.8+)")
    else:
        print("   ⚠️  Python 3.8 or higher is recommended")
    
    print("\n" + "=" * 60)
    
    # Exit code
    sys.exit(0 if not missing_required else 1)


if __name__ == "__main__":
    main()
