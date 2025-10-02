"""
Depth and volume calculation module
Calculate mining depth and excavation volume using DEM data
"""

import numpy as np
from shapely.geometry import Polygon
from scipy import interpolate
from typing import List, Dict, Tuple, Optional
import rasterio
from rasterio.mask import mask as rasterio_mask


class DepthVolumeCalculator:
    """Calculate mining depth and volume from DEM data"""
    
    def __init__(self, dem: np.ndarray, dem_metadata: Dict, 
                 pixel_size: float = 30.0):
        """
        Initialize DepthVolumeCalculator
        
        Args:
            dem: Digital Elevation Model array
            dem_metadata: DEM metadata including transform and CRS
            pixel_size: Size of each DEM pixel in meters
        """
        self.dem = dem
        self.dem_metadata = dem_metadata
        self.pixel_size = pixel_size
        self.transform = dem_metadata.get('transform')
    
    def estimate_reference_elevation(self, polygon: Polygon, 
                                    method: str = 'mean',
                                    buffer_distance: float = 50) -> float:
        """
        Estimate reference elevation (pre-mining ground level) around mining area
        
        Args:
            polygon: Mining area polygon (in pixel coordinates)
            method: Method to estimate reference ('mean', 'median', 'max', 'percentile')
            buffer_distance: Distance in pixels to sample around mining area
            
        Returns:
            Reference elevation in meters
        """
        # Create buffer around polygon to sample reference elevation
        buffered = polygon.buffer(buffer_distance)
        
        # Create a mask for the buffer zone (excluding the mining area itself)
        buffer_zone = buffered.difference(polygon)
        
        # Sample elevation values from buffer zone
        elevations = []
        
        # Get bounds
        minx, miny, maxx, maxy = buffer_zone.bounds
        minx, miny = int(max(0, minx)), int(max(0, miny))
        maxx, maxy = int(min(self.dem.shape[1], maxx)), int(min(self.dem.shape[0], maxy))
        
        # Sample points in the buffer zone
        for y in range(miny, maxy):
            for x in range(minx, maxx):
                from shapely.geometry import Point
                if buffer_zone.contains(Point(x, y)):
                    elevation = self.dem[y, x]
                    if elevation > 0:  # Exclude nodata values
                        elevations.append(elevation)
        
        if not elevations:
            # Fallback: use mean of surrounding area
            crop = self.dem[miny:maxy, minx:maxx]
            elevations = crop[crop > 0].flatten()
        
        if len(elevations) == 0:
            return 0.0
        
        # Calculate reference based on method
        if method == 'mean':
            return float(np.mean(elevations))
        elif method == 'median':
            return float(np.median(elevations))
        elif method == 'max':
            return float(np.max(elevations))
        elif method == 'percentile':
            return float(np.percentile(elevations, 75))  # 75th percentile
        else:
            return float(np.mean(elevations))
    
    def calculate_depth_map(self, polygon: Polygon, 
                           reference_elevation: float) -> Tuple[np.ndarray, Dict]:
        """
        Calculate depth map for a mining area
        
        Args:
            polygon: Mining area polygon
            reference_elevation: Reference elevation for depth calculation
            
        Returns:
            Tuple of (depth map array, statistics dict)
        """
        # Get bounds
        minx, miny, maxx, maxy = polygon.bounds
        minx, miny = int(max(0, minx)), int(max(0, miny))
        maxx, maxy = int(min(self.dem.shape[1], maxx)), int(min(self.dem.shape[0], maxy))
        
        # Create depth map
        depth_map = np.zeros((maxy - miny, maxx - minx))
        
        # Calculate depth for each pixel
        for y in range(miny, maxy):
            for x in range(minx, maxx):
                from shapely.geometry import Point
                if polygon.contains(Point(x, y)):
                    elevation = self.dem[y, x]
                    depth = reference_elevation - elevation
                    depth_map[y - miny, x - minx] = max(0, depth)  # Only positive depths
        
        # Calculate statistics
        valid_depths = depth_map[depth_map > 0]
        
        if len(valid_depths) > 0:
            stats = {
                'mean_depth': float(np.mean(valid_depths)),
                'max_depth': float(np.max(valid_depths)),
                'min_depth': float(np.min(valid_depths)),
                'std_depth': float(np.std(valid_depths)),
                'reference_elevation': reference_elevation
            }
        else:
            stats = {
                'mean_depth': 0.0,
                'max_depth': 0.0,
                'min_depth': 0.0,
                'std_depth': 0.0,
                'reference_elevation': reference_elevation
            }
        
        return depth_map, stats
    
    def calculate_volume_simpsons(self, depth_map: np.ndarray) -> float:
        """
        Calculate excavation volume using Simpson's rule
        
        Args:
            depth_map: Depth map array
            
        Returns:
            Volume in cubic meters
        """
        h, w = depth_map.shape
        
        if h < 3 or w < 3:
            # Fallback to trapezoidal for small areas
            return self.calculate_volume_trapezoidal(depth_map)
        
        # Ensure odd number of points for Simpson's rule
        if h % 2 == 0:
            depth_map = depth_map[:-1, :]
            h -= 1
        if w % 2 == 0:
            depth_map = depth_map[:, :-1]
            w -= 1
        
        # Apply Simpson's 1/3 rule in 2D
        volume = 0.0
        
        # Simpson's coefficients
        for i in range(0, h, 2):
            for j in range(0, w, 2):
                if i + 2 < h and j + 2 < w:
                    # 3x3 block
                    block = depth_map[i:i+3, j:j+3]
                    
                    # Simpson's 2D weights
                    weights = np.array([
                        [1, 4, 1],
                        [4, 16, 4],
                        [1, 4, 1]
                    ])
                    
                    block_volume = np.sum(block * weights)
                    volume += block_volume
        
        # Multiply by grid spacing
        # Simpson's rule: (h*k/9) * sum
        volume = volume * (self.pixel_size ** 2) / 9
        
        return float(volume)
    
    def calculate_volume_trapezoidal(self, depth_map: np.ndarray) -> float:
        """
        Calculate excavation volume using trapezoidal rule (fallback method)
        
        Args:
            depth_map: Depth map array
            
        Returns:
            Volume in cubic meters
        """
        # Simple trapezoidal integration
        # Volume ≈ sum of depths * pixel area
        total_depth = np.sum(depth_map)
        pixel_area = self.pixel_size ** 2
        volume = total_depth * pixel_area
        
        return float(volume)
    
    def calculate_volume_montecarlo(self, depth_map: np.ndarray, 
                                   n_samples: int = 10000) -> float:
        """
        Calculate volume using Monte Carlo integration
        
        Args:
            depth_map: Depth map array
            n_samples: Number of random samples
            
        Returns:
            Volume in cubic meters
        """
        h, w = depth_map.shape
        
        # Random sampling
        total_depth = 0.0
        for _ in range(n_samples):
            i = np.random.randint(0, h)
            j = np.random.randint(0, w)
            total_depth += depth_map[i, j]
        
        # Average depth * total area
        avg_depth = total_depth / n_samples
        total_area = h * w * (self.pixel_size ** 2)
        volume = avg_depth * total_area
        
        return float(volume)
    
    def process_mining_polygon(self, polygon: Polygon,
                              reference_method: str = 'mean',
                              volume_method: str = 'simpsons') -> Dict:
        """
        Process a single mining polygon to calculate depth and volume
        
        Args:
            polygon: Mining area polygon
            reference_method: Method to estimate reference elevation
            volume_method: Method to calculate volume ('simpsons', 'trapezoidal', 'montecarlo')
            
        Returns:
            Dictionary containing results
        """
        # Estimate reference elevation
        reference_elevation = self.estimate_reference_elevation(
            polygon, method=reference_method
        )
        
        # Calculate depth map
        depth_map, depth_stats = self.calculate_depth_map(polygon, reference_elevation)
        
        # Calculate volume
        if volume_method == 'simpsons':
            volume = self.calculate_volume_simpsons(depth_map)
        elif volume_method == 'trapezoidal':
            volume = self.calculate_volume_trapezoidal(depth_map)
        elif volume_method == 'montecarlo':
            volume = self.calculate_volume_montecarlo(depth_map)
        else:
            volume = self.calculate_volume_simpsons(depth_map)
        
        # Calculate area
        area_sqm = polygon.area * (self.pixel_size ** 2)
        
        # Compile results
        results = {
            'polygon': polygon,
            'depth_map': depth_map,
            'depth_statistics': depth_stats,
            'volume_cubic_meters': volume,
            'volume_cubic_feet': volume * 35.3147,  # Conversion
            'area_square_meters': area_sqm,
            'area_hectares': area_sqm / 10000,
            'average_depth_meters': depth_stats['mean_depth'],
            'max_depth_meters': depth_stats['max_depth'],
            'reference_elevation': reference_elevation
        }
        
        return results
    
    def process_multiple_polygons(self, polygons: List[Polygon],
                                 reference_method: str = 'mean',
                                 volume_method: str = 'simpsons') -> List[Dict]:
        """
        Process multiple mining polygons
        
        Args:
            polygons: List of mining polygons
            reference_method: Reference elevation method
            volume_method: Volume calculation method
            
        Returns:
            List of result dictionaries
        """
        results = []
        
        for i, polygon in enumerate(polygons):
            print(f"Processing polygon {i+1}/{len(polygons)}...")
            result = self.process_mining_polygon(
                polygon, reference_method, volume_method
            )
            result['id'] = i + 1
            results.append(result)
        
        return results
    
    def aggregate_results(self, results: List[Dict]) -> Dict:
        """
        Aggregate results from multiple mining areas
        
        Args:
            results: List of individual polygon results
            
        Returns:
            Aggregated statistics
        """
        total_volume = sum(r['volume_cubic_meters'] for r in results)
        total_area = sum(r['area_square_meters'] for r in results)
        avg_depth = np.mean([r['average_depth_meters'] for r in results])
        max_depth = max(r['max_depth_meters'] for r in results)
        
        aggregate = {
            'total_number_of_mines': len(results),
            'total_excavation_volume_cubic_meters': total_volume,
            'total_excavation_volume_cubic_feet': total_volume * 35.3147,
            'total_mining_area_square_meters': total_area,
            'total_mining_area_hectares': total_area / 10000,
            'average_depth_across_all_mines': avg_depth,
            'maximum_depth_across_all_mines': max_depth,
            'average_volume_per_mine': total_volume / len(results) if results else 0
        }
        
        return aggregate
    
    def export_depth_map(self, depth_map: np.ndarray, 
                        output_path: str,
                        bounds: Tuple[float, float, float, float],
                        crs: Optional = None):
        """
        Export depth map as GeoTIFF
        
        Args:
            depth_map: Depth map array
            output_path: Output file path
            bounds: Geographic bounds
            crs: Coordinate reference system
        """
        from rasterio.transform import from_bounds
        
        h, w = depth_map.shape
        transform = from_bounds(*bounds, w, h)
        
        with rasterio.open(
            output_path,
            'w',
            driver='GTiff',
            height=h,
            width=w,
            count=1,
            dtype=depth_map.dtype,
            crs=crs,
            transform=transform
        ) as dst:
            dst.write(depth_map, 1)
        
        print(f"Exported depth map to {output_path}")
