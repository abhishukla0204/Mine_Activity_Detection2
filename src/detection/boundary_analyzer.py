"""
Boundary comparison module
Compares detected mining areas with authorized boundaries
"""

import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, shape
from shapely.ops import unary_union
from typing import List, Dict, Tuple, Optional
import fiona


class BoundaryAnalyzer:
    """Analyze mining activity relative to authorized boundaries"""
    
    def __init__(self, authorized_boundary_path: Optional[str] = None):
        """
        Initialize BoundaryAnalyzer
        
        Args:
            authorized_boundary_path: Path to authorized boundary shapefile/KML
        """
        self.authorized_boundary = None
        
        if authorized_boundary_path:
            self.load_authorized_boundary(authorized_boundary_path)
    
    def load_authorized_boundary(self, boundary_path: str):
        """
        Load authorized mining boundary from shapefile or KML
        
        Args:
            boundary_path: Path to boundary file
        """
        # Read using geopandas (supports shapefile, GeoJSON, KML, etc.)
        gdf = gpd.read_file(boundary_path)
        
        # Combine all geometries into a single polygon/multipolygon
        self.authorized_boundary = unary_union(gdf.geometry)
        
        print(f"Loaded authorized boundary: {self.authorized_boundary.area:.2f} sq units")
    
    def create_rectangular_boundary(self, bounds: Tuple[float, float, float, float]) -> Polygon:
        """
        Create a rectangular boundary from bounds (for testing)
        
        Args:
            bounds: (minx, miny, maxx, maxy)
            
        Returns:
            Polygon representing the boundary
        """
        minx, miny, maxx, maxy = bounds
        return Polygon([
            (minx, miny),
            (maxx, miny),
            (maxx, maxy),
            (minx, maxy),
            (minx, miny)
        ])
    
    def classify_mining_areas(self, detected_polygons: List[Polygon],
                             authorized_boundary: Optional[Polygon] = None) -> Dict:
        """
        Classify mining areas as legal (inside boundary) or illegal (outside)
        
        Args:
            detected_polygons: List of detected mining polygons
            authorized_boundary: Authorized boundary polygon (optional, uses loaded if None)
            
        Returns:
            Dictionary containing legal and illegal polygons with statistics
        """
        if authorized_boundary is None:
            authorized_boundary = self.authorized_boundary
        
        if authorized_boundary is None:
            raise ValueError("No authorized boundary provided or loaded")
        
        legal_polygons = []
        illegal_polygons = []
        partial_polygons = []
        
        for poly in detected_polygons:
            # Check intersection with authorized boundary
            intersection = poly.intersection(authorized_boundary)
            intersection_area = intersection.area if intersection else 0
            
            # Calculate percentage inside boundary
            if poly.area > 0:
                inside_percentage = (intersection_area / poly.area) * 100
            else:
                inside_percentage = 0
            
            if inside_percentage >= 95:  # Fully inside (allowing 5% tolerance)
                legal_polygons.append(poly)
            elif inside_percentage <= 5:  # Fully outside
                illegal_polygons.append(poly)
            else:  # Partially inside/outside
                partial_polygons.append({
                    'polygon': poly,
                    'inside_area': intersection_area,
                    'outside_area': poly.area - intersection_area,
                    'inside_percentage': inside_percentage,
                    'inside_part': intersection,
                    'outside_part': poly.difference(authorized_boundary)
                })
        
        return {
            'legal': legal_polygons,
            'illegal': illegal_polygons,
            'partial': partial_polygons,
            'authorized_boundary': authorized_boundary
        }
    
    def calculate_area_statistics(self, classification_result: Dict, 
                                  pixel_size: float = 10.0) -> Dict:
        """
        Calculate detailed statistics for classified mining areas
        
        Args:
            classification_result: Result from classify_mining_areas
            pixel_size: Size of each pixel in meters
            
        Returns:
            Dictionary containing statistics
        """
        legal_polys = classification_result['legal']
        illegal_polys = classification_result['illegal']
        partial_polys = classification_result['partial']
        
        # Calculate total areas
        legal_area = sum(p.area for p in legal_polys) * (pixel_size ** 2)
        illegal_area = sum(p.area for p in illegal_polys) * (pixel_size ** 2)
        
        # Add partial areas
        partial_inside_area = sum(p['inside_area'] for p in partial_polys) * (pixel_size ** 2)
        partial_outside_area = sum(p['outside_area'] for p in partial_polys) * (pixel_size ** 2)
        
        total_legal_area = legal_area + partial_inside_area
        total_illegal_area = illegal_area + partial_outside_area
        total_mining_area = total_legal_area + total_illegal_area
        
        # Calculate authorized boundary area
        authorized_area = classification_result['authorized_boundary'].area * (pixel_size ** 2)
        
        # Calculate percentages
        if authorized_area > 0:
            utilization_percentage = (total_legal_area / authorized_area) * 100
        else:
            utilization_percentage = 0
        
        if total_mining_area > 0:
            illegal_percentage = (total_illegal_area / total_mining_area) * 100
        else:
            illegal_percentage = 0
        
        stats = {
            'total_mining_area_sqm': total_mining_area,
            'total_mining_area_hectares': total_mining_area / 10000,
            'legal_mining_area_sqm': total_legal_area,
            'legal_mining_area_hectares': total_legal_area / 10000,
            'illegal_mining_area_sqm': total_illegal_area,
            'illegal_mining_area_hectares': total_illegal_area / 10000,
            'authorized_area_sqm': authorized_area,
            'authorized_area_hectares': authorized_area / 10000,
            'authorized_utilization_percentage': utilization_percentage,
            'illegal_mining_percentage': illegal_percentage,
            'num_legal_sites': len(legal_polys),
            'num_illegal_sites': len(illegal_polys),
            'num_partial_sites': len(partial_polys),
            'total_mining_sites': len(legal_polys) + len(illegal_polys) + len(partial_polys)
        }
        
        return stats
    
    def generate_violation_report(self, classification_result: Dict,
                                  statistics: Dict) -> List[Dict]:
        """
        Generate detailed violation report for illegal mining activities
        
        Args:
            classification_result: Classification result
            statistics: Area statistics
            
        Returns:
            List of violation records
        """
        violations = []
        
        # Fully illegal sites
        for i, poly in enumerate(classification_result['illegal']):
            centroid = poly.centroid
            violations.append({
                'violation_id': f"ILLEGAL_{i+1}",
                'type': 'fully_outside',
                'area_sqm': poly.area * 100,  # Assuming pixel_size=10m
                'area_hectares': poly.area * 100 / 10000,
                'centroid_x': centroid.x,
                'centroid_y': centroid.y,
                'severity': 'high',
                'polygon': poly
            })
        
        # Partial violations
        for i, partial in enumerate(classification_result['partial']):
            centroid = partial['polygon'].centroid
            violations.append({
                'violation_id': f"PARTIAL_{i+1}",
                'type': 'partially_outside',
                'total_area_sqm': partial['polygon'].area * 100,
                'outside_area_sqm': partial['outside_area'] * 100,
                'outside_area_hectares': partial['outside_area'] * 100 / 10000,
                'outside_percentage': 100 - partial['inside_percentage'],
                'centroid_x': centroid.x,
                'centroid_y': centroid.y,
                'severity': 'medium' if partial['inside_percentage'] > 50 else 'high',
                'polygon': partial['polygon'],
                'outside_polygon': partial['outside_part']
            })
        
        return violations
    
    def export_classification_results(self, classification_result: Dict,
                                     output_dir: str,
                                     crs: str = None):
        """
        Export classification results to separate files
        
        Args:
            classification_result: Classification result
            output_dir: Output directory path
            crs: Coordinate reference system
        """
        from pathlib import Path
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Export legal mining areas
        if classification_result['legal']:
            legal_gdf = gpd.GeoDataFrame(
                {'type': 'legal'}, 
                geometry=classification_result['legal'],
                crs=crs
            )
            legal_gdf.to_file(output_dir / 'legal_mining_areas.geojson', driver='GeoJSON')
        
        # Export illegal mining areas
        if classification_result['illegal']:
            illegal_gdf = gpd.GeoDataFrame(
                {'type': 'illegal'},
                geometry=classification_result['illegal'],
                crs=crs
            )
            illegal_gdf.to_file(output_dir / 'illegal_mining_areas.geojson', driver='GeoJSON')
        
        # Export partial mining areas
        if classification_result['partial']:
            partial_data = []
            for p in classification_result['partial']:
                partial_data.append({
                    'geometry': p['polygon'],
                    'inside_percentage': p['inside_percentage'],
                    'outside_area': p['outside_area']
                })
            
            partial_gdf = gpd.GeoDataFrame(partial_data, crs=crs)
            partial_gdf.to_file(output_dir / 'partial_mining_areas.geojson', driver='GeoJSON')
        
        # Export authorized boundary
        boundary_gdf = gpd.GeoDataFrame(
            {'type': 'authorized_boundary'},
            geometry=[classification_result['authorized_boundary']],
            crs=crs
        )
        boundary_gdf.to_file(output_dir / 'authorized_boundary.geojson', driver='GeoJSON')
        
        print(f"Exported classification results to {output_dir}")
    
    def visualize_classification(self, image: np.ndarray, 
                                classification_result: Dict,
                                output_path: Optional[str] = None) -> np.ndarray:
        """
        Visualize classification on image
        
        Args:
            image: Background image
            classification_result: Classification result
            output_path: Optional path to save visualization
            
        Returns:
            Visualized image
        """
        import cv2
        
        # Create a copy
        vis_image = image.copy()
        
        # Ensure 3-channel
        if len(vis_image.shape) == 2:
            vis_image = cv2.cvtColor(vis_image, cv2.COLOR_GRAY2BGR)
        
        # Draw authorized boundary (blue)
        boundary = classification_result['authorized_boundary']
        if boundary.geom_type == 'Polygon':
            coords = np.array(boundary.exterior.coords, dtype=np.int32)
            cv2.polylines(vis_image, [coords], True, (255, 255, 0), 3)
        
        # Draw legal mining (green)
        for poly in classification_result['legal']:
            coords = np.array(poly.exterior.coords, dtype=np.int32)
            overlay = vis_image.copy()
            cv2.fillPoly(overlay, [coords], (0, 255, 0))
            cv2.addWeighted(overlay, 0.3, vis_image, 0.7, 0, vis_image)
            cv2.polylines(vis_image, [coords], True, (0, 200, 0), 2)
        
        # Draw illegal mining (red)
        for poly in classification_result['illegal']:
            coords = np.array(poly.exterior.coords, dtype=np.int32)
            overlay = vis_image.copy()
            cv2.fillPoly(overlay, [coords], (0, 0, 255))
            cv2.addWeighted(overlay, 0.4, vis_image, 0.6, 0, vis_image)
            cv2.polylines(vis_image, [coords], True, (0, 0, 200), 2)
        
        # Draw partial mining (orange)
        for partial in classification_result['partial']:
            poly = partial['polygon']
            coords = np.array(poly.exterior.coords, dtype=np.int32)
            overlay = vis_image.copy()
            cv2.fillPoly(overlay, [coords], (0, 165, 255))
            cv2.addWeighted(overlay, 0.3, vis_image, 0.7, 0, vis_image)
            cv2.polylines(vis_image, [coords], True, (0, 140, 255), 2)
        
        # Add legend
        legend_y = 30
        cv2.rectangle(vis_image, (10, 10), (250, legend_y * 5), (255, 255, 255), -1)
        cv2.rectangle(vis_image, (10, 10), (250, legend_y * 5), (0, 0, 0), 2)
        cv2.putText(vis_image, "Authorized Boundary", (20, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        cv2.putText(vis_image, "Legal Mining", (20, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(vis_image, "Illegal Mining", (20, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(vis_image, "Partial Violation", (20, 120),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2)
        
        if output_path:
            cv2.imwrite(output_path, cv2.cvtColor(vis_image, cv2.COLOR_RGB2BGR))
        
        return vis_image
