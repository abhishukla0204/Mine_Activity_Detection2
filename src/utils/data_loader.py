"""
Data loader module for satellite imagery, DEM, and annotation data
"""

import json
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from PIL import Image
import cv2
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class DataLoader:
    """Load and preprocess geospatial data for mining activity analysis"""
    
    def __init__(self, data_dir: str):
        """
        Initialize DataLoader
        
        Args:
            data_dir: Path to the data directory
        """
        self.data_dir = Path(data_dir)
        
    def load_satellite_image(self, tif_path: str) -> Tuple[np.ndarray, Dict]:
        """
        Load satellite image from TIF file
        
        Args:
            tif_path: Path to the TIF file
            
        Returns:
            Tuple of (image array, metadata dict)
        """
        with rasterio.open(tif_path) as src:
            # Read all bands
            image = src.read()
            
            # Get metadata
            metadata = {
                'crs': src.crs,
                'transform': src.transform,
                'bounds': src.bounds,
                'width': src.width,
                'height': src.height,
                'count': src.count,
                'dtype': src.dtypes[0],
                'nodata': src.nodata
            }
            
            # Transpose to (height, width, channels) for easier processing
            if image.shape[0] < image.shape[1]:  # If channels are first dimension
                image = np.transpose(image, (1, 2, 0))
            
        return image, metadata
    
    def load_dem(self, dem_path: str) -> Tuple[np.ndarray, Dict]:
        """
        Load Digital Elevation Model from TIF file
        
        Args:
            dem_path: Path to the DEM TIF file
            
        Returns:
            Tuple of (DEM array, metadata dict)
        """
        with rasterio.open(dem_path) as src:
            dem = src.read(1)  # Read first band
            
            metadata = {
                'crs': src.crs,
                'transform': src.transform,
                'bounds': src.bounds,
                'width': src.width,
                'height': src.height,
                'dtype': src.dtypes[0],
                'nodata': src.nodata
            }
            
        return dem, metadata
    
    def resample_dem_to_image(self, dem: np.ndarray, dem_meta: Dict, 
                              target_meta: Dict) -> np.ndarray:
        """
        Resample DEM to match satellite image resolution and extent
        
        Args:
            dem: DEM array
            dem_meta: DEM metadata
            target_meta: Target image metadata
            
        Returns:
            Resampled DEM array
        """
        # Calculate transform for reprojection
        transform, width, height = calculate_default_transform(
            dem_meta['crs'], target_meta['crs'],
            dem_meta['width'], dem_meta['height'],
            *dem_meta['bounds']
        )
        
        # Create destination array
        resampled_dem = np.zeros((target_meta['height'], target_meta['width']), 
                                 dtype=dem.dtype)
        
        # Reproject
        reproject(
            source=dem,
            destination=resampled_dem,
            src_transform=dem_meta['transform'],
            src_crs=dem_meta['crs'],
            dst_transform=target_meta['transform'],
            dst_crs=target_meta['crs'],
            resampling=Resampling.bilinear
        )
        
        return resampled_dem
    
    def load_coco_annotations(self, json_path: str) -> Dict:
        """
        Load COCO format annotations
        
        Args:
            json_path: Path to COCO JSON file
            
        Returns:
            Dictionary containing annotations, images, and categories
        """
        with open(json_path, 'r') as f:
            coco_data = json.load(f)
        
        return coco_data
    
    def coco_to_polygons(self, coco_data: Dict, image_width: int, 
                         image_height: int) -> List[Dict]:
        """
        Convert COCO annotations to polygon format
        
        Args:
            coco_data: COCO annotation dictionary
            image_width: Width of the image
            image_height: Height of the image
            
        Returns:
            List of polygons with metadata
        """
        polygons = []
        
        # Get category mapping
        categories = {cat['id']: cat['name'] for cat in coco_data['categories']}
        
        for ann in coco_data['annotations']:
            if 'segmentation' in ann:
                segmentation = ann['segmentation'][0]  # Get first segmentation
                
                # Reshape to (n, 2) for polygon coordinates
                points = np.array(segmentation).reshape(-1, 2)
                
                polygon_data = {
                    'id': ann['id'],
                    'category_id': ann['category_id'],
                    'category_name': categories.get(ann['category_id'], 'unknown'),
                    'points': points,
                    'bbox': ann['bbox'],  # [x, y, width, height]
                    'area': ann['area']
                }
                
                polygons.append(polygon_data)
        
        return polygons
    
    def create_mask_from_polygons(self, polygons: List[Dict], 
                                   width: int, height: int) -> np.ndarray:
        """
        Create binary mask from polygons
        
        Args:
            polygons: List of polygon dictionaries
            width: Width of the mask
            height: Height of the mask
            
        Returns:
            Binary mask array
        """
        mask = np.zeros((height, width), dtype=np.uint8)
        
        for poly in polygons:
            points = poly['points'].astype(np.int32)
            cv2.fillPoly(mask, [points], 255)
        
        return mask
    
    def normalize_image(self, image: np.ndarray, 
                       percentile_clip: Tuple[float, float] = (2, 98)) -> np.ndarray:
        """
        Normalize image for visualization
        
        Args:
            image: Input image array
            percentile_clip: Tuple of (min_percentile, max_percentile) for clipping
            
        Returns:
            Normalized image (0-255 uint8)
        """
        normalized = np.zeros_like(image, dtype=np.uint8)
        
        for i in range(image.shape[-1] if len(image.shape) == 3 else 1):
            if len(image.shape) == 3:
                band = image[:, :, i]
            else:
                band = image
            
            # Clip outliers
            vmin, vmax = np.percentile(band[band > 0], percentile_clip)
            band_clipped = np.clip(band, vmin, vmax)
            
            # Normalize to 0-255
            band_norm = ((band_clipped - vmin) / (vmax - vmin) * 255).astype(np.uint8)
            
            if len(image.shape) == 3:
                normalized[:, :, i] = band_norm
            else:
                normalized = band_norm
        
        return normalized
    
    def load_reference_image(self, image_path: str) -> np.ndarray:
        """
        Load reference JPEG image
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Image array
        """
        image = Image.open(image_path)
        return np.array(image)


def pixel_to_geo_coords(pixel_x: int, pixel_y: int, 
                        transform: rasterio.Affine) -> Tuple[float, float]:
    """
    Convert pixel coordinates to geographic coordinates
    
    Args:
        pixel_x: Pixel x coordinate
        pixel_y: Pixel y coordinate
        transform: Rasterio transform object
        
    Returns:
        Tuple of (longitude, latitude) or (easting, northing)
    """
    geo_x, geo_y = transform * (pixel_x, pixel_y)
    return geo_x, geo_y


def geo_to_pixel_coords(geo_x: float, geo_y: float, 
                        transform: rasterio.Affine) -> Tuple[int, int]:
    """
    Convert geographic coordinates to pixel coordinates
    
    Args:
        geo_x: Geographic x coordinate (longitude or easting)
        geo_y: Geographic y coordinate (latitude or northing)
        transform: Rasterio transform object
        
    Returns:
        Tuple of (pixel_x, pixel_y)
    """
    inv_transform = ~transform
    pixel_x, pixel_y = inv_transform * (geo_x, geo_y)
    return int(pixel_x), int(pixel_y)
