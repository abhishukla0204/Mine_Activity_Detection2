"""
Mining area detection module
Detects and extracts mining areas from satellite imagery
"""

import numpy as np
import cv2
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import rasterio
from rasterio.features import shapes


class MiningDetector:
    """Detect mining areas from satellite imagery and annotations"""
    
    def __init__(self, config: Dict = None):
        """
        Initialize MiningDetector
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.min_area = self.config.get('min_area', 100)
    
    def detect_from_annotations(self, coco_data: Dict, image_shape: Tuple[int, int]) -> List[Polygon]:
        """
        Extract mining areas from COCO annotations
        
        Args:
            coco_data: COCO format annotations
            image_shape: Shape of the image (height, width)
            
        Returns:
            List of Shapely Polygon objects representing mines
        """
        polygons = []
        height, width = image_shape
        
        # Get category mapping
        categories = {cat['id']: cat['name'] for cat in coco_data['categories']}
        
        for ann in coco_data['annotations']:
            if 'segmentation' in ann:
                segmentation = ann['segmentation'][0]
                
                # Convert to polygon coordinates
                points = np.array(segmentation).reshape(-1, 2)
                
                # Create Shapely polygon
                if len(points) >= 3:  # Need at least 3 points for polygon
                    poly = Polygon(points)
                    
                    # Check if valid and meets minimum area
                    if poly.is_valid and poly.area >= self.min_area:
                        polygons.append(poly)
        
        return polygons
    
    def detect_from_image(self, image: np.ndarray, method: str = 'supervised') -> List[Polygon]:
        """
        Detect mining areas directly from satellite image using computer vision
        
        Args:
            image: Satellite image array
            method: Detection method ('supervised', 'unsupervised', 'threshold')
            
        Returns:
            List of detected mining polygons
        """
        if method == 'threshold':
            return self._threshold_based_detection(image)
        elif method == 'unsupervised':
            return self._clustering_based_detection(image)
        else:
            raise ValueError(f"Unsupported detection method: {method}")
    
    def _threshold_based_detection(self, image: np.ndarray) -> List[Polygon]:
        """
        Simple threshold-based mining detection
        (Mines typically have lower vegetation and different spectral signature)
        
        Args:
            image: RGB satellite image
            
        Returns:
            List of detected polygons
        """
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        # Apply adaptive threshold
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Morphological operations to clean up
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Convert to polygons
        polygons = []
        for contour in contours:
            if cv2.contourArea(contour) >= self.min_area:
                # Approximate contour
                epsilon = 0.01 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Convert to Shapely polygon
                points = approx.reshape(-1, 2)
                if len(points) >= 3:
                    poly = Polygon(points)
                    if poly.is_valid:
                        polygons.append(poly)
        
        return polygons
    
    def _clustering_based_detection(self, image: np.ndarray, n_clusters: int = 5) -> List[Polygon]:
        """
        Clustering-based mining detection using K-means
        
        Args:
            image: Satellite image
            n_clusters: Number of clusters
            
        Returns:
            List of detected polygons
        """
        from sklearn.cluster import KMeans
        
        # Reshape image for clustering
        h, w = image.shape[:2]
        if len(image.shape) == 3:
            pixels = image.reshape(-1, image.shape[2])
        else:
            pixels = image.reshape(-1, 1)
        
        # Apply K-means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(pixels)
        
        # Reshape back to image
        segmented = labels.reshape(h, w)
        
        # Extract mining areas (assume they are in specific clusters)
        # This is a simplified approach - you may need domain knowledge
        # to identify which cluster represents mining
        polygons = []
        for cluster_id in range(n_clusters):
            mask = (segmented == cluster_id).astype(np.uint8) * 255
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                if cv2.contourArea(contour) >= self.min_area:
                    epsilon = 0.01 * cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, epsilon, True)
                    
                    points = approx.reshape(-1, 2)
                    if len(points) >= 3:
                        poly = Polygon(points)
                        if poly.is_valid:
                            polygons.append(poly)
        
        return polygons
    
    def merge_overlapping_polygons(self, polygons: List[Polygon], 
                                   buffer_distance: float = 0.5) -> List[Polygon]:
        """
        Merge overlapping or nearby polygons
        
        Args:
            polygons: List of input polygons
            buffer_distance: Distance to buffer polygons before merging
            
        Returns:
            List of merged polygons
        """
        if not polygons:
            return []
        
        # Buffer polygons slightly
        buffered = [poly.buffer(buffer_distance) for poly in polygons]
        
        # Union all polygons
        merged = unary_union(buffered)
        
        # Remove buffer
        result = merged.buffer(-buffer_distance)
        
        # Convert to list
        if isinstance(result, Polygon):
            return [result]
        elif isinstance(result, MultiPolygon):
            return list(result.geoms)
        else:
            return []
    
    def calculate_polygon_metrics(self, polygons: List[Polygon], 
                                  pixel_size: float = 10.0) -> List[Dict]:
        """
        Calculate metrics for each detected polygon
        
        Args:
            polygons: List of polygons
            pixel_size: Size of each pixel in meters (default 10m for Sentinel-2)
            
        Returns:
            List of metric dictionaries
        """
        metrics = []
        
        for i, poly in enumerate(polygons):
            # Calculate area in square meters
            area_pixels = poly.area
            area_sqm = area_pixels * (pixel_size ** 2)
            area_hectares = area_sqm / 10000
            
            # Get bounds
            minx, miny, maxx, maxy = poly.bounds
            
            # Calculate perimeter
            perimeter_pixels = poly.length
            perimeter_m = perimeter_pixels * pixel_size
            
            # Calculate centroid
            centroid = poly.centroid
            
            metrics.append({
                'id': i,
                'area_pixels': area_pixels,
                'area_sqm': area_sqm,
                'area_hectares': area_hectares,
                'perimeter_pixels': perimeter_pixels,
                'perimeter_m': perimeter_m,
                'centroid_x': centroid.x,
                'centroid_y': centroid.y,
                'bounds': (minx, miny, maxx, maxy),
                'polygon': poly
            })
        
        return metrics
    
    def export_polygons_to_geojson(self, polygons: List[Polygon], 
                                   output_path: str, 
                                   transform: Optional = None,
                                   crs: Optional = None):
        """
        Export polygons to GeoJSON file
        
        Args:
            polygons: List of polygons
            output_path: Output file path
            transform: Rasterio transform to convert pixel to geo coordinates
            crs: Coordinate reference system
        """
        import geopandas as gpd
        
        if not polygons:
            print("No polygons to export")
            return
        
        # Create GeoDataFrame
        gdf = gpd.GeoDataFrame({'geometry': polygons}, crs=crs)
        
        # If transform is provided, convert coordinates
        if transform is not None:
            # The polygons are already in pixel coordinates
            # GeoDataFrame will handle the coordinate system
            pass
        
        # Save to file
        gdf.to_file(output_path, driver='GeoJSON')
        print(f"Exported {len(polygons)} polygons to {output_path}")
    
    def visualize_detections(self, image: np.ndarray, polygons: List[Polygon], 
                            output_path: Optional[str] = None) -> np.ndarray:
        """
        Visualize detected polygons on image
        
        Args:
            image: Original image
            polygons: List of detected polygons
            output_path: Optional path to save visualization
            
        Returns:
            Visualized image
        """
        # Create a copy of the image
        vis_image = image.copy()
        
        # Ensure image is 3-channel
        if len(vis_image.shape) == 2:
            vis_image = cv2.cvtColor(vis_image, cv2.COLOR_GRAY2BGR)
        
        # Draw polygons
        for i, poly in enumerate(polygons):
            # Get exterior coordinates
            coords = np.array(poly.exterior.coords, dtype=np.int32)
            
            # Draw filled polygon with transparency
            overlay = vis_image.copy()
            cv2.fillPoly(overlay, [coords], (0, 255, 0))
            cv2.addWeighted(overlay, 0.3, vis_image, 0.7, 0, vis_image)
            
            # Draw outline
            cv2.polylines(vis_image, [coords], True, (255, 0, 0), 2)
            
            # Add label
            centroid = poly.centroid
            cv2.putText(vis_image, f"Mine {i+1}", 
                       (int(centroid.x), int(centroid.y)),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # Save if output path provided
        if output_path:
            cv2.imwrite(output_path, cv2.cvtColor(vis_image, cv2.COLOR_RGB2BGR))
        
        return vis_image
