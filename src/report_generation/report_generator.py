"""
Report generation module
Generate comprehensive reports for mining activity monitoring
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import json
import base64
from io import BytesIO


class ReportGenerator:
    """Generate comprehensive mining activity reports"""
    
    def __init__(self, output_dir: str = "outputs/reports"):
        """
        Initialize Report Generator
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.report_data = {}
    
    def compile_report_data(self, 
                           classification_result: Dict,
                           statistics: Dict,
                           depth_results: List[Dict],
                           violations: List[Dict],
                           metadata: Dict = None):
        """
        Compile all data for report generation
        
        Args:
            classification_result: Mining area classification
            statistics: Statistical summary
            depth_results: Depth and volume calculations
            violations: List of violations
            metadata: Additional metadata
        """
        self.report_data = {
            'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'classification': classification_result,
            'statistics': statistics,
            'depth_results': depth_results,
            'violations': violations,
            'metadata': metadata or {}
        }
    
    def generate_html_report(self, output_filename: str = None) -> str:
        """
        Generate HTML report
        
        Args:
            output_filename: Optional custom filename
            
        Returns:
            Path to generated report
        """
        if output_filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"mining_activity_report_{timestamp}.html"
        
        output_path = self.output_dir / output_filename
        
        # Generate HTML content
        html_content = self._create_html_template()
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Generated HTML report: {output_path}")
        return str(output_path)
    
    def _create_html_template(self) -> str:
        """Create HTML report template"""
        
        stats = self.report_data.get('statistics', {})
        violations = self.report_data.get('violations', [])
        depth_results = self.report_data.get('depth_results', [])
        
        # Calculate aggregate depth/volume stats
        if depth_results:
            total_volume = sum(r['volume_cubic_meters'] for r in depth_results)
            avg_depth = sum(r['average_depth_meters'] for r in depth_results) / len(depth_results)
            max_depth = max(r['max_depth_meters'] for r in depth_results)
        else:
            total_volume = avg_depth = max_depth = 0
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mining Activity Monitoring Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .section {{
            background: white;
            padding: 30px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .section h2 {{
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        
        .stat-card.warning {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        
        .stat-card.success {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }}
        
        .stat-card h3 {{
            font-size: 1em;
            margin-bottom: 10px;
            opacity: 0.9;
        }}
        
        .stat-card .value {{
            font-size: 2em;
            font-weight: bold;
        }}
        
        .stat-card .unit {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        th {{
            background-color: #667eea;
            color: white;
            font-weight: bold;
        }}
        
        tr:hover {{
            background-color: #f5f5f5;
        }}
        
        .violation-high {{
            color: #f5576c;
            font-weight: bold;
        }}
        
        .violation-medium {{
            color: #ffa502;
            font-weight: bold;
        }}
        
        .alert {{
            background-color: #fee;
            border-left: 4px solid #f5576c;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        
        .alert h3 {{
            color: #f5576c;
            margin-bottom: 10px;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }}
        
        @media print {{
            body {{
                background: white;
            }}
            
            .section {{
                box-shadow: none;
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏔️ Mining Activity Monitoring Report</h1>
            <p>Generated on {self.report_data.get('generation_date', 'N/A')}</p>
            <p>Comprehensive Analysis of Open Cast Mining Activities</p>
        </div>
        
        <!-- Executive Summary -->
        <div class="section">
            <h2>📊 Executive Summary</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>Total Mining Area</h3>
                    <div class="value">{stats.get('total_mining_area_hectares', 0):.2f}</div>
                    <div class="unit">hectares</div>
                </div>
                
                <div class="stat-card success">
                    <h3>Legal Mining Area</h3>
                    <div class="value">{stats.get('legal_mining_area_hectares', 0):.2f}</div>
                    <div class="unit">hectares</div>
                </div>
                
                <div class="stat-card warning">
                    <h3>Illegal Mining Area</h3>
                    <div class="value">{stats.get('illegal_mining_area_hectares', 0):.2f}</div>
                    <div class="unit">hectares</div>
                </div>
                
                <div class="stat-card warning">
                    <h3>Illegal Mining %</h3>
                    <div class="value">{stats.get('illegal_mining_percentage', 0):.1f}%</div>
                    <div class="unit">of total</div>
                </div>
                
                <div class="stat-card">
                    <h3>Total Excavation Volume</h3>
                    <div class="value">{total_volume:,.0f}</div>
                    <div class="unit">cubic meters</div>
                </div>
                
                <div class="stat-card">
                    <h3>Average Mining Depth</h3>
                    <div class="value">{avg_depth:.1f}</div>
                    <div class="unit">meters</div>
                </div>
                
                <div class="stat-card">
                    <h3>Maximum Depth</h3>
                    <div class="value">{max_depth:.1f}</div>
                    <div class="unit">meters</div>
                </div>
                
                <div class="stat-card">
                    <h3>Total Mining Sites</h3>
                    <div class="value">{stats.get('total_mining_sites', 0)}</div>
                    <div class="unit">sites</div>
                </div>
            </div>
        </div>
        
        <!-- Violations Alert -->
        {self._generate_violations_section(violations)}
        
        <!-- Detailed Statistics -->
        <div class="section">
            <h2>📈 Detailed Mining Statistics</h2>
            
            <h3>Area Breakdown</h3>
            <table>
                <tr>
                    <th>Category</th>
                    <th>Number of Sites</th>
                    <th>Area (hectares)</th>
                    <th>Area (sq. meters)</th>
                    <th>Percentage</th>
                </tr>
                <tr>
                    <td>Legal Mining (Within Boundary)</td>
                    <td>{stats.get('num_legal_sites', 0)}</td>
                    <td>{stats.get('legal_mining_area_hectares', 0):.2f}</td>
                    <td>{stats.get('legal_mining_area_sqm', 0):,.2f}</td>
                    <td>{100 - stats.get('illegal_mining_percentage', 0):.1f}%</td>
                </tr>
                <tr>
                    <td>Illegal Mining (Outside Boundary)</td>
                    <td>{stats.get('num_illegal_sites', 0)}</td>
                    <td>{stats.get('illegal_mining_area_hectares', 0):.2f}</td>
                    <td>{stats.get('illegal_mining_area_sqm', 0):,.2f}</td>
                    <td>{stats.get('illegal_mining_percentage', 0):.1f}%</td>
                </tr>
                <tr>
                    <td>Partial Violations</td>
                    <td>{stats.get('num_partial_sites', 0)}</td>
                    <td>-</td>
                    <td>-</td>
                    <td>-</td>
                </tr>
                <tr style="font-weight: bold; background-color: #f0f0f0;">
                    <td>TOTAL</td>
                    <td>{stats.get('total_mining_sites', 0)}</td>
                    <td>{stats.get('total_mining_area_hectares', 0):.2f}</td>
                    <td>{stats.get('total_mining_area_sqm', 0):,.2f}</td>
                    <td>100%</td>
                </tr>
            </table>
            
            <h3 style="margin-top: 30px;">Depth and Volume Analysis</h3>
            <table>
                <tr>
                    <th>Mine ID</th>
                    <th>Area (ha)</th>
                    <th>Avg Depth (m)</th>
                    <th>Max Depth (m)</th>
                    <th>Volume (m³)</th>
                    <th>Volume (ft³)</th>
                </tr>
                {self._generate_depth_table_rows(depth_results)}
            </table>
        </div>
        
        <!-- Violations Details -->
        {self._generate_violations_detail_section(violations)}
        
        <!-- Recommendations -->
        <div class="section">
            <h2>💡 Recommendations</h2>
            <ol>
                {self._generate_recommendations(stats, violations)}
            </ol>
        </div>
        
        <!-- Metadata -->
        <div class="section">
            <h2>ℹ️ Report Metadata</h2>
            <table>
                <tr>
                    <td><strong>Report Generation Date</strong></td>
                    <td>{self.report_data.get('generation_date', 'N/A')}</td>
                </tr>
                <tr>
                    <td><strong>Analysis Method</strong></td>
                    <td>Satellite Imagery Analysis with DEM Integration</td>
                </tr>
                <tr>
                    <td><strong>Data Sources</strong></td>
                    <td>Sentinel-2 (10m), SRTM DEM (30m), COCO Annotations</td>
                </tr>
                <tr>
                    <td><strong>Volume Calculation Method</strong></td>
                    <td>Simpson's Rule for Numerical Integration</td>
                </tr>
            </table>
        </div>
        
        <div class="footer">
            <p>This report was automatically generated by the Mining Activity Monitoring Tool</p>
            <p>© {datetime.now().year} - For Official Use Only</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _generate_violations_section(self, violations: List[Dict]) -> str:
        """Generate violations alert section"""
        if not violations:
            return """
        <div class="section" style="background-color: #e8f5e9;">
            <h2 style="color: #4caf50;">✅ Compliance Status: CLEAR</h2>
            <p>No violations detected. All mining activities are within authorized boundaries.</p>
        </div>
            """
        
        high_severity = sum(1 for v in violations if v.get('severity') == 'high')
        medium_severity = sum(1 for v in violations if v.get('severity') == 'medium')
        
        return f"""
        <div class="alert">
            <h3>⚠️ VIOLATIONS DETECTED</h3>
            <p><strong>{len(violations)}</strong> violation(s) found:</p>
            <ul>
                <li><strong class="violation-high">{high_severity}</strong> High Severity Violations</li>
                <li><strong class="violation-medium">{medium_severity}</strong> Medium Severity Violations</li>
            </ul>
            <p>Immediate action required to address illegal mining activities.</p>
        </div>
        """
    
    def _generate_violations_detail_section(self, violations: List[Dict]) -> str:
        """Generate detailed violations section"""
        if not violations:
            return ""
        
        rows = ""
        for v in violations:
            if v['type'] == 'fully_outside':
                rows += f"""
                <tr>
                    <td>{v['violation_id']}</td>
                    <td class="violation-{v['severity'].lower()}">Fully Outside Boundary</td>
                    <td>{v['area_hectares']:.2f}</td>
                    <td>100%</td>
                    <td>({v['centroid_x']:.1f}, {v['centroid_y']:.1f})</td>
                    <td class="violation-{v['severity'].lower()}">{v['severity'].upper()}</td>
                </tr>
                """
            else:
                rows += f"""
                <tr>
                    <td>{v['violation_id']}</td>
                    <td class="violation-{v['severity'].lower()}">Partially Outside</td>
                    <td>{v['outside_area_hectares']:.2f}</td>
                    <td>{v['outside_percentage']:.1f}%</td>
                    <td>({v['centroid_x']:.1f}, {v['centroid_y']:.1f})</td>
                    <td class="violation-{v['severity'].lower()}">{v['severity'].upper()}</td>
                </tr>
                """
        
        return f"""
        <div class="section">
            <h2>🚨 Violation Details</h2>
            <table>
                <tr>
                    <th>Violation ID</th>
                    <th>Type</th>
                    <th>Illegal Area (ha)</th>
                    <th>Outside %</th>
                    <th>Location (x, y)</th>
                    <th>Severity</th>
                </tr>
                {rows}
            </table>
        </div>
        """
    
    def _generate_depth_table_rows(self, depth_results: List[Dict]) -> str:
        """Generate table rows for depth results"""
        rows = ""
        for r in depth_results[:20]:  # Limit to first 20
            rows += f"""
                <tr>
                    <td>Mine {r['id']}</td>
                    <td>{r['area_hectares']:.2f}</td>
                    <td>{r['average_depth_meters']:.1f}</td>
                    <td>{r['max_depth_meters']:.1f}</td>
                    <td>{r['volume_cubic_meters']:,.0f}</td>
                    <td>{r['volume_cubic_feet']:,.0f}</td>
                </tr>
            """
        return rows
    
    def _generate_recommendations(self, stats: Dict, violations: List[Dict]) -> str:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if violations:
            recommendations.append(
                "<li><strong>URGENT:</strong> Conduct immediate field inspection of "
                f"{len(violations)} identified violation sites.</li>"
            )
            recommendations.append(
                "<li>Issue notices to mining operators for unauthorized excavations "
                "outside the permitted boundary.</li>"
            )
        
        if stats.get('illegal_mining_percentage', 0) > 10:
            recommendations.append(
                "<li>Implement stricter monitoring and enforcement measures. "
                f"Current illegal mining rate ({stats.get('illegal_mining_percentage', 0):.1f}%) "
                "exceeds acceptable limits.</li>"
            )
        
        if stats.get('total_mining_sites', 0) > 10:
            recommendations.append(
                "<li>Consider consolidation of smaller mining operations to improve "
                "regulatory oversight and environmental management.</li>"
            )
        
        recommendations.append(
            "<li>Continue regular satellite-based monitoring (quarterly recommended) "
            "to detect unauthorized expansions early.</li>"
        )
        
        recommendations.append(
            "<li>Update DEM data annually to track cumulative excavation volumes "
            "and ensure proper mine closure planning.</li>"
        )
        
        if not violations:
            recommendations.append(
                "<li>Maintain current compliance status through ongoing monitoring "
                "and stakeholder engagement.</li>"
            )
        
        return "\n".join(recommendations)
    
    def export_json_data(self, output_filename: str = None) -> str:
        """
        Export report data as JSON
        
        Args:
            output_filename: Optional custom filename
            
        Returns:
            Path to JSON file
        """
        if output_filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"mining_data_{timestamp}.json"
        
        output_path = self.output_dir / output_filename
        
        # Convert non-serializable objects
        export_data = {
            'generation_date': self.report_data.get('generation_date'),
            'statistics': self.report_data.get('statistics', {}),
            'violations': self.report_data.get('violations', []),
            'depth_summary': [
                {
                    'id': r['id'],
                    'area_hectares': r['area_hectares'],
                    'average_depth': r['average_depth_meters'],
                    'max_depth': r['max_depth_meters'],
                    'volume_m3': r['volume_cubic_meters']
                }
                for r in self.report_data.get('depth_results', [])
            ]
        }
        
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"Exported JSON data to {output_path}")
        return str(output_path)
