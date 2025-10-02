"""
2D Map visualization module using Folium and Plotly
"""

import folium
from folium import plugins
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from shapely.geometry import Polygon
from typing import List, Dict, Tuple, Optional
import json


class Map2DVisualizer:
    """Create interactive 2D maps for mining activity visualization"""
    
    def __init__(self, center_coords: Tuple[float, float] = None,
                 zoom_start: int = 12):
        """
        Initialize 2D Map Visualizer
        
        Args:
            center_coords: (latitude, longitude) for map center
            zoom_start: Initial zoom level
        """
        self.center_coords = center_coords or (24.0, 82.5)  # Default: Singrauli area
        self.zoom_start = zoom_start
    
    def create_folium_map(self, satellite_bounds: Tuple = None) -> folium.Map:
        """
        Create base Folium map
        
        Args:
            satellite_bounds: Bounds for map extent
            
        Returns:
            Folium Map object
        """
        # Create map
        m = folium.Map(
            location=self.center_coords,
            zoom_start=self.zoom_start,
            tiles='OpenStreetMap'
        )
        
        # Add different tile layers
        folium.TileLayer('Stamen Terrain').add_to(m)
        folium.TileLayer('Stamen Toner').add_to(m)
        folium.TileLayer('CartoDB positron').add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        return m
    
    def add_polygons_to_map(self, m: folium.Map, polygons: List[Polygon],
                           color: str = 'blue', name: str = 'Polygons',
                           popup_info: List[Dict] = None) -> folium.Map:
        """
        Add polygons to Folium map
        
        Args:
            m: Folium map object
            polygons: List of Shapely polygons
            color: Color for polygons
            name: Layer name
            popup_info: Optional list of popup information dicts
            
        Returns:
            Updated Folium map
        """
        feature_group = folium.FeatureGroup(name=name)
        
        for i, poly in enumerate(polygons):
            # Get coordinates
            coords = list(poly.exterior.coords)
            # Convert to (lat, lon) - note: may need coordinate transformation
            folium_coords = [(y, x) for x, y in coords]
            
            # Create popup
            if popup_info and i < len(popup_info):
                popup_text = "<br>".join([f"<b>{k}</b>: {v}" for k, v in popup_info[i].items()])
            else:
                popup_text = f"Area {i+1}"
            
            # Add polygon
            folium.Polygon(
                locations=folium_coords,
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.3,
                weight=2,
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(feature_group)
        
        feature_group.add_to(m)
        return m
    
    def create_classification_map(self, classification_result: Dict,
                                  statistics: Dict,
                                  output_path: str = None) -> folium.Map:
        """
        Create map showing legal vs illegal mining areas
        
        Args:
            classification_result: Classification results
            statistics: Area statistics
            output_path: Optional path to save HTML
            
        Returns:
            Folium map
        """
        m = self.create_folium_map()
        
        # Add authorized boundary
        boundary = classification_result['authorized_boundary']
        if boundary.geom_type == 'Polygon':
            coords = list(boundary.exterior.coords)
            folium_coords = [(y, x) for x, y in coords]
            
            folium.Polygon(
                locations=folium_coords,
                color='yellow',
                fill=False,
                weight=3,
                popup='Authorized Mining Boundary'
            ).add_to(m)
        
        # Add legal mining areas (green)
        if classification_result['legal']:
            legal_info = [{'Type': 'Legal Mining', 'Status': 'Within Boundary'} 
                         for _ in classification_result['legal']]
            self.add_polygons_to_map(m, classification_result['legal'], 
                                    color='green', name='Legal Mining',
                                    popup_info=legal_info)
        
        # Add illegal mining areas (red)
        if classification_result['illegal']:
            illegal_info = [{'Type': 'ILLEGAL Mining', 'Status': 'Outside Boundary',
                           'Severity': 'HIGH'} 
                          for _ in classification_result['illegal']]
            self.add_polygons_to_map(m, classification_result['illegal'],
                                    color='red', name='Illegal Mining',
                                    popup_info=illegal_info)
        
        # Add partial violations (orange)
        if classification_result['partial']:
            partial_polys = [p['polygon'] for p in classification_result['partial']]
            partial_info = [
                {
                    'Type': 'Partial Violation',
                    'Inside %': f"{p['inside_percentage']:.1f}%",
                    'Outside Area (ha)': f"{p['outside_area']*100/10000:.2f}",
                    'Severity': 'MEDIUM' if p['inside_percentage'] > 50 else 'HIGH'
                }
                for p in classification_result['partial']
            ]
            self.add_polygons_to_map(m, partial_polys,
                                    color='orange', name='Partial Violations',
                                    popup_info=partial_info)
        
        # Add statistics panel
        stats_html = f"""
        <div style="position: fixed; 
                    top: 10px; right: 10px; width: 300px; 
                    background-color: white; border: 2px solid black;
                    z-index: 9999; font-size: 14px; padding: 10px;">
            <h4>Mining Activity Summary</h4>
            <b>Total Mining Area:</b> {statistics['total_mining_area_hectares']:.2f} ha<br>
            <b>Legal Mining:</b> {statistics['legal_mining_area_hectares']:.2f} ha<br>
            <b style="color: red;">Illegal Mining:</b> {statistics['illegal_mining_area_hectares']:.2f} ha<br>
            <b>Illegal %:</b> {statistics['illegal_mining_percentage']:.1f}%<br>
            <b>Total Sites:</b> {statistics['total_mining_sites']}<br>
            <b>Legal Sites:</b> {statistics['num_legal_sites']}<br>
            <b style="color: red;">Illegal Sites:</b> {statistics['num_illegal_sites']}<br>
        </div>
        """
        m.get_root().html.add_child(folium.Element(stats_html))
        
        # Save if path provided
        if output_path:
            m.save(output_path)
            print(f"Saved 2D map to {output_path}")
        
        return m
    
    def create_depth_heatmap(self, depth_results: List[Dict],
                            output_path: str = None):
        """
        Create heatmap visualization of mining depths
        
        Args:
            depth_results: List of depth calculation results
            output_path: Optional path to save HTML
            
        Returns:
            Plotly figure
        """
        # Prepare data
        mine_ids = [f"Mine {r['id']}" for r in depth_results]
        avg_depths = [r['average_depth_meters'] for r in depth_results]
        max_depths = [r['max_depth_meters'] for r in depth_results]
        volumes = [r['volume_cubic_meters'] for r in depth_results]
        
        # Create figure with subplots
        fig = go.Figure()
        
        # Add average depth bars
        fig.add_trace(go.Bar(
            x=mine_ids,
            y=avg_depths,
            name='Average Depth (m)',
            marker_color='lightblue'
        ))
        
        # Add max depth bars
        fig.add_trace(go.Bar(
            x=mine_ids,
            y=max_depths,
            name='Maximum Depth (m)',
            marker_color='darkblue'
        ))
        
        fig.update_layout(
            title='Mining Depth Analysis',
            xaxis_title='Mining Site',
            yaxis_title='Depth (meters)',
            barmode='group',
            height=500
        )
        
        if output_path:
            fig.write_html(output_path)
            print(f"Saved depth heatmap to {output_path}")
        
        return fig
    
    def create_volume_chart(self, depth_results: List[Dict],
                           output_path: str = None):
        """
        Create chart showing excavation volumes
        
        Args:
            depth_results: List of depth calculation results
            output_path: Optional path to save HTML
            
        Returns:
            Plotly figure
        """
        mine_ids = [f"Mine {r['id']}" for r in depth_results]
        volumes = [r['volume_cubic_meters'] for r in depth_results]
        areas = [r['area_hectares'] for r in depth_results]
        
        # Create figure
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=mine_ids,
            y=volumes,
            name='Excavation Volume (m³)',
            marker_color='brown',
            text=[f"{v:,.0f} m³" for v in volumes],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Excavation Volume by Mining Site',
            xaxis_title='Mining Site',
            yaxis_title='Volume (cubic meters)',
            height=500,
            showlegend=True
        )
        
        if output_path:
            fig.write_html(output_path)
            print(f"Saved volume chart to {output_path}")
        
        return fig
    
    def create_overview_dashboard(self, classification_result: Dict,
                                 statistics: Dict,
                                 depth_results: List[Dict],
                                 output_path: str = None):
        """
        Create comprehensive dashboard with multiple visualizations
        
        Args:
            classification_result: Classification results
            statistics: Statistics dictionary
            depth_results: Depth calculation results
            output_path: Optional path to save HTML
            
        Returns:
            Plotly figure
        """
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Mining Area Distribution', 'Depth Analysis',
                          'Volume Distribution', 'Compliance Status'),
            specs=[[{'type': 'pie'}, {'type': 'bar'}],
                   [{'type': 'bar'}, {'type': 'pie'}]]
        )
        
        # 1. Area distribution pie chart
        fig.add_trace(
            go.Pie(
                labels=['Legal Mining', 'Illegal Mining'],
                values=[statistics['legal_mining_area_hectares'],
                       statistics['illegal_mining_area_hectares']],
                marker_colors=['green', 'red']
            ),
            row=1, col=1
        )
        
        # 2. Depth bar chart
        mine_ids = [f"M{r['id']}" for r in depth_results[:10]]  # Limit to 10
        depths = [r['average_depth_meters'] for r in depth_results[:10]]
        
        fig.add_trace(
            go.Bar(
                x=mine_ids,
                y=depths,
                marker_color='blue',
                name='Avg Depth'
            ),
            row=1, col=2
        )
        
        # 3. Volume bar chart
        volumes = [r['volume_cubic_meters']/1000 for r in depth_results[:10]]  # in thousands
        
        fig.add_trace(
            go.Bar(
                x=mine_ids,
                y=volumes,
                marker_color='brown',
                name='Volume (×1000 m³)'
            ),
            row=2, col=1
        )
        
        # 4. Compliance pie chart
        fig.add_trace(
            go.Pie(
                labels=['Legal Sites', 'Illegal Sites', 'Partial Violations'],
                values=[statistics['num_legal_sites'],
                       statistics['num_illegal_sites'],
                       statistics['num_partial_sites']],
                marker_colors=['green', 'red', 'orange']
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            height=800,
            showlegend=True,
            title_text="Mining Activity Monitoring Dashboard"
        )
        
        if output_path:
            fig.write_html(output_path)
            print(f"Saved dashboard to {output_path}")
        
        return fig
