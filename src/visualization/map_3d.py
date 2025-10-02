"""
3D visualization module using PyVista and Plotly
"""

import numpy as np
import plotly.graph_objects as go
from shapely.geometry import Polygon
from typing import List, Dict, Tuple, Optional
try:
    import pyvista as pv
except ImportError:
    pv = None


class Map3DVisualizer:
    """Create 3D visualizations of mining areas with DEM"""
    
    def __init__(self, vertical_exaggeration: float = 3.0):
        """
        Initialize 3D visualizer
        
        Args:
            vertical_exaggeration: Factor to exaggerate elevation for better visualization
        """
        self.vertical_exaggeration = vertical_exaggeration
    
    def create_plotly_3d_surface(self, dem: np.ndarray,
                                 polygons: List[Polygon] = None,
                                 output_path: str = None) -> go.Figure:
        """
        Create 3D surface plot using Plotly
        
        Args:
            dem: Digital Elevation Model array
            polygons: Optional list of mining polygons to highlight
            output_path: Optional path to save HTML
            
        Returns:
            Plotly Figure
        """
        h, w = dem.shape
        
        # Create coordinate grids
        x = np.arange(w)
        y = np.arange(h)
        X, Y = np.meshgrid(x, y)
        
        # Apply vertical exaggeration
        Z = dem * self.vertical_exaggeration
        
        # Create surface plot
        fig = go.Figure(data=[
            go.Surface(
                x=X, y=Y, z=Z,
                colorscale='terrain',
                name='Terrain'
            )
        ])
        
        # Add mining polygons as overlays
        if polygons:
            for i, poly in enumerate(polygons):
                coords = np.array(poly.exterior.coords)
                px, py = coords[:, 0], coords[:, 1]
                
                # Get elevation at polygon points
                pz = []
                for x, y in zip(px, py):
                    if 0 <= int(y) < h and 0 <= int(x) < w:
                        pz.append(dem[int(y), int(x)] * self.vertical_exaggeration)
                    else:
                        pz.append(0)
                
                # Add polygon outline
                fig.add_trace(go.Scatter3d(
                    x=px, y=py, z=pz,
                    mode='lines',
                    line=dict(color='red', width=5),
                    name=f'Mine {i+1}'
                ))
        
        # Update layout
        fig.update_layout(
            title='3D Terrain Visualization with Mining Areas',
            scene=dict(
                xaxis_title='X (pixels)',
                yaxis_title='Y (pixels)',
                zaxis_title='Elevation (m)',
                aspectmode='manual',
                aspectratio=dict(x=2, y=2, z=0.5)
            ),
            height=700
        )
        
        if output_path:
            fig.write_html(output_path)
            print(f"Saved 3D surface plot to {output_path}")
        
        return fig
    
    def create_depth_profile_3d(self, depth_results: List[Dict],
                               output_path: str = None) -> go.Figure:
        """
        Create 3D visualization of depth profiles
        
        Args:
            depth_results: List of depth calculation results
            output_path: Optional path to save HTML
            
        Returns:
            Plotly Figure
        """
        fig = go.Figure()
        
        for result in depth_results:
            depth_map = result['depth_map']
            mine_id = result['id']
            
            h, w = depth_map.shape
            x = np.arange(w)
            y = np.arange(h)
            X, Y = np.meshgrid(x, y)
            Z = -depth_map  # Negative for excavation
            
            # Add surface for this mine
            fig.add_trace(go.Surface(
                x=X + (mine_id * w * 1.2),  # Offset each mine
                y=Y,
                z=Z,
                colorscale='Reds',
                name=f'Mine {mine_id}',
                showscale=(mine_id == 1)
            ))
        
        fig.update_layout(
            title='3D Depth Profiles of Mining Areas',
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Depth (m, negative)',
                aspectmode='auto'
            ),
            height=700
        )
        
        if output_path:
            fig.write_html(output_path)
            print(f"Saved 3D depth profile to {output_path}")
        
        return fig
    
    def create_pyvista_visualization(self, dem: np.ndarray,
                                    polygons: List[Polygon] = None,
                                    depth_maps: List[np.ndarray] = None,
                                    output_path: str = None):
        """
        Create advanced 3D visualization using PyVista
        
        Args:
            dem: Digital Elevation Model
            polygons: Mining polygons
            depth_maps: List of depth maps
            output_path: Optional path to save (screenshot or HTML)
        """
        if pv is None:
            print("PyVista not available. Install with: pip install pyvista")
            return None
        
        # Create plotter
        plotter = pv.Plotter(off_screen=(output_path is not None))
        
        # Create structured grid from DEM
        h, w = dem.shape
        x = np.arange(w)
        y = np.arange(h)
        X, Y = np.meshgrid(x, y)
        Z = dem * self.vertical_exaggeration
        
        # Create surface
        grid = pv.StructuredGrid(X, Y, Z)
        
        # Add DEM surface
        plotter.add_mesh(
            grid,
            scalars=Z.flatten(),
            cmap='terrain',
            show_edges=False,
            opacity=0.9,
            name='terrain'
        )
        
        # Add mining polygons as tubes
        if polygons:
            for i, poly in enumerate(polygons):
                coords = np.array(poly.exterior.coords)
                px, py = coords[:, 0], coords[:, 1]
                
                # Get elevation
                pz = []
                for x, y in zip(px, py):
                    if 0 <= int(y) < h and 0 <= int(x) < w:
                        pz.append(dem[int(y), int(x)] * self.vertical_exaggeration + 10)
                    else:
                        pz.append(10)
                
                # Create polyline
                points = np.column_stack([px, py, pz])
                polyline = pv.lines_from_points(points, close=True)
                
                # Add as tube for better visibility
                tube = polyline.tube(radius=5)
                plotter.add_mesh(tube, color='red', opacity=0.8)
        
        # Set view
        plotter.camera_position = 'iso'
        plotter.show_grid()
        plotter.add_axes()
        
        if output_path:
            if output_path.endswith('.png'):
                plotter.screenshot(output_path)
            else:
                plotter.export_html(output_path)
            print(f"Saved PyVista visualization to {output_path}")
        else:
            plotter.show()
        
        return plotter
    
    def create_volumetric_visualization(self, dem: np.ndarray,
                                       depth_maps: List[np.ndarray],
                                       output_path: str = None):
        """
        Create volumetric visualization showing excavation
        
        Args:
            dem: Original DEM
            depth_maps: List of depth maps for mining areas
            output_path: Optional output path
            
        Returns:
            Plotly Figure
        """
        # Combine all depth maps
        h, w = dem.shape
        combined_depth = np.zeros((h, w))
        
        for depth_map in depth_maps:
            dh, dw = depth_map.shape
            # Place depth map at appropriate location (simplified)
            if dh <= h and dw <= w:
                combined_depth[:dh, :dw] = np.maximum(
                    combined_depth[:dh, :dw],
                    depth_map
                )
        
        # Create figure with original and excavated surfaces
        fig = go.Figure()
        
        x = np.arange(w)
        y = np.arange(h)
        X, Y = np.meshgrid(x, y)
        
        # Original surface
        Z_original = dem * self.vertical_exaggeration
        fig.add_trace(go.Surface(
            x=X, y=Y, z=Z_original,
            colorscale='Greens',
            name='Original Ground',
            opacity=0.7,
            showscale=False
        ))
        
        # Excavated surface
        Z_excavated = (dem - combined_depth) * self.vertical_exaggeration
        fig.add_trace(go.Surface(
            x=X, y=Y, z=Z_excavated,
            colorscale='Reds',
            name='Excavated Surface',
            opacity=0.8
        ))
        
        fig.update_layout(
            title='Volumetric Excavation Visualization',
            scene=dict(
                xaxis_title='X (pixels)',
                yaxis_title='Y (pixels)',
                zaxis_title='Elevation (m)',
                aspectmode='manual',
                aspectratio=dict(x=2, y=2, z=0.5)
            ),
            height=700
        )
        
        if output_path:
            fig.write_html(output_path)
            print(f"Saved volumetric visualization to {output_path}")
        
        return fig
