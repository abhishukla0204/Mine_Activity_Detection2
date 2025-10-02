"""
Configuration management for the mining monitoring tool
"""

import yaml
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration class for managing project settings"""
    
    # Default configuration
    DEFAULT_CONFIG = {
        'data': {
            'singrauli_dir': 'data/Singrauli',
            'satellite_image': 'Singrauli_Sentinel2_RGB.tif',
            'dem_file': 'Singrauli_SRTM_DEM.tif',
            'reference_image': 'Singrauli_mines_image.jpeg',
            'annotations_file': 'mine_shape/_annotations.coco.json',
            'boundary_shapefile': None,  # Optional: authorized mining boundary
        },
        'processing': {
            'resample_dem': True,
            'normalize_images': True,
            'percentile_clip': [2, 98],
        },
        'detection': {
            'min_area': 100,  # Minimum mining area in pixels
            'use_coco_annotations': True,
        },
        'depth_volume': {
            'reference_elevation': 'mean',  # 'mean', 'median', or numeric value
            'volume_method': 'simpsons',  # 'simpsons', 'trapezoidal'
            'num_intervals': 100,  # For numerical integration
        },
        'visualization': {
            '2d_map': {
                'basemap': 'OpenStreetMap',
                'zoom_start': 12,
            },
            '3d_view': {
                'vertical_exaggeration': 3.0,
                'colormap': 'terrain',
            }
        },
        'report': {
            'output_dir': 'outputs/reports',
            'format': 'html',  # 'html', 'pdf', or 'both'
            'include_3d': True,
            'include_statistics': True,
        },
        'output': {
            'save_intermediate': True,
            'visualization_dir': 'outputs/visualizations',
        }
    }
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to YAML config file (optional)
        """
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_path and Path(config_path).exists():
            self.load_from_file(config_path)
    
    def load_from_file(self, config_path: str):
        """
        Load configuration from YAML file
        
        Args:
            config_path: Path to YAML config file
        """
        with open(config_path, 'r') as f:
            user_config = yaml.safe_load(f)
        
        # Update default config with user config
        self._update_dict(self.config, user_config)
    
    def _update_dict(self, base_dict: Dict, update_dict: Dict):
        """Recursively update nested dictionary"""
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict:
                self._update_dict(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def save_to_file(self, config_path: str):
        """
        Save current configuration to YAML file
        
        Args:
            config_path: Path to save YAML config file
        """
        with open(config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key_path: Dot-separated path to config value (e.g., 'data.satellite_image')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """
        Set configuration value using dot notation
        
        Args:
            key_path: Dot-separated path to config value
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
