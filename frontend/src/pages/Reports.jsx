import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FileText, Download, Calendar, MapPin, BarChart3, AlertTriangle } from 'lucide-react'

const Reports = () => {
  const [miningData, setMiningData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Load actual mining metrics
    fetch('/computed_metrics.json')
      .then(res => res.json())
      .then(data => {
        setMiningData(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error loading metrics:', err)
        setLoading(false)
      })
  }, [])

  if (loading || !miningData) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <FileText className="w-12 h-12 mx-auto mb-4 text-primary-400 animate-pulse" />
          <p className="text-dark-muted">Loading report data...</p>
        </div>
      </div>
    )
  }

  const { metadata, mines } = miningData

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-4xl font-bold gradient-text mb-2">
          Analysis Reports
        </h1>
        <p className="text-dark-muted">
          Comprehensive mining activity assessment and compliance documentation
        </p>
      </div>

      {/* Report Summary Card */}
      <div className="card bg-gradient-to-br from-primary-500/10 to-accent-purple/10 border-primary-500/30">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h2 className="text-2xl font-bold mb-4">Singrauli Mining Assessment Report</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div>
                <p className="text-sm text-dark-muted mb-1">Report Date</p>
                <p className="font-semibold flex items-center">
                  <Calendar className="w-4 h-4 mr-2" />
                  {metadata.computation_date}
                </p>
              </div>
              <div>
                <p className="text-sm text-dark-muted mb-1">Region</p>
                <p className="font-semibold flex items-center">
                  <MapPin className="w-4 h-4 mr-2" />
                  Singrauli, MP
                </p>
              </div>
              <div>
                <p className="text-sm text-dark-muted mb-1">Sites Analyzed</p>
                <p className="font-semibold flex items-center">
                  <BarChart3 className="w-4 h-4 mr-2" />
                  {metadata.total_mines} sites
                </p>
              </div>
              <div>
                <p className="text-sm text-dark-muted mb-1">Violations</p>
                <p className="font-semibold flex items-center text-red-400">
                  <AlertTriangle className="w-4 h-4 mr-2" />
                  {metadata.illegal_mines} sites
                </p>
              </div>
            </div>
          </div>
          <button className="btn-primary ml-4">
            <Download className="w-5 h-5 inline mr-2" />
            Download PDF
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Detailed Analysis */}
        <div className="lg:col-span-2 space-y-6">
          {/* Executive Summary */}
          <div className="card">
            <h3 className="text-xl font-bold mb-4">Executive Summary</h3>
            <div className="space-y-4">
              <p className="text-dark-muted leading-relaxed">
                This comprehensive assessment analyzes {metadata.total_mines} mining sites across the Singrauli region 
                using high-resolution satellite imagery and Digital Elevation Model (DEM) data.
              </p>
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-dark-elevated rounded-lg">
                  <p className="text-sm text-dark-muted mb-2">Total Excavation Area</p>
                  <p className="text-2xl font-bold gradient-text">
                    {(metadata.total_area_hectares / 1000).toFixed(2)} km²
                  </p>
                </div>
                <div className="p-4 bg-dark-elevated rounded-lg">
                  <p className="text-sm text-dark-muted mb-2">Total Volume Extracted</p>
                  <p className="text-2xl font-bold gradient-text">
                    {(metadata.total_volume_m3 / 1000000000).toFixed(2)} B m³
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Compliance Status */}
          <div className="card">
            <h3 className="text-xl font-bold mb-4">Compliance Status</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-green-500/10 rounded-lg border border-green-500/30">
                <div>
                  <p className="font-semibold text-green-400">Authorized Operations</p>
                  <p className="text-sm text-dark-muted mt-1">Licensed mining sites operating within boundaries</p>
                </div>
                <div className="text-right">
                  <p className="text-3xl font-bold text-green-400">{metadata.legal_mines}</p>
                  <p className="text-sm text-dark-muted">sites</p>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-4 bg-red-500/10 rounded-lg border border-red-500/30">
                <div>
                  <p className="font-semibold text-red-400">Unauthorized Activities</p>
                  <p className="text-sm text-dark-muted mt-1">Detected illegal excavation requiring intervention</p>
                </div>
                <div className="text-right">
                  <p className="text-3xl font-bold text-red-400">{metadata.illegal_mines}</p>
                  <p className="text-sm text-dark-muted">violations</p>
                </div>
              </div>
            </div>
          </div>

          {/* Site-wise Breakdown */}
          <div className="card">
            <h3 className="text-xl font-bold mb-4">Site-wise Analysis</h3>
            <div className="space-y-3">
              {mines.slice(0, 5).map((mine) => (
                <div key={mine.id} className="p-4 bg-dark-elevated rounded-lg">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h4 className="font-semibold">Mining Site #{mine.id}</h4>
                      <p className="text-sm text-dark-muted">{mine.operator}</p>
                    </div>
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        mine.type === 'legal'
                          ? 'bg-green-500/20 text-green-400'
                          : 'bg-red-500/20 text-red-400'
                      }`}
                    >
                      {mine.type === 'legal' ? 'Authorized' : 'Unauthorized'}
                    </span>
                  </div>
                  <div className="grid grid-cols-3 gap-4 mt-3 text-sm">
                    <div>
                      <p className="text-dark-muted">Area</p>
                      <p className="font-semibold">{mine.area_hectares.toFixed(1)} ha</p>
                    </div>
                    <div>
                      <p className="text-dark-muted">Depth</p>
                      <p className="font-semibold">{mine.depth_m.toFixed(0)} m</p>
                    </div>
                    <div>
                      <p className="text-dark-muted">Volume</p>
                      <p className="font-semibold">{(mine.volume_m3 / 1000000).toFixed(1)}M m³</p>
                    </div>
                  </div>
                </div>
              ))}
              <p className="text-center text-dark-muted text-sm">
                View full site list on the{' '}
                <a href="/" className="text-primary-400 hover:underline">Dashboard</a>
              </p>
            </div>
          </div>
        </div>

        {/* Sidebar - Quick Actions */}
        <div className="space-y-6">
          {/* Data Source */}
          <div className="card">
            <h3 className="font-bold mb-4">Data Sources</h3>
            <div className="space-y-3 text-sm">
              <div>
                <p className="text-dark-muted">Satellite Imagery</p>
                <p className="font-medium">Sentinel-2 RGB</p>
              </div>
              <div>
                <p className="text-dark-muted">Elevation Data</p>
                <p className="font-medium">SRTM DEM</p>
              </div>
              <div>
                <p className="text-dark-muted">Analysis Date</p>
                <p className="font-medium">{metadata.computation_date}</p>
              </div>
            </div>
          </div>

          {/* Export Options */}
          <div className="card">
            <h3 className="font-bold mb-4">Export Options</h3>
            <div className="space-y-2">
              <button className="btn-primary w-full justify-center">
                <Download className="w-4 h-4 inline mr-2" />
                Download Full Report (PDF)
              </button>
              <button className="btn-secondary w-full justify-center">
                Export Data (JSON)
              </button>
              <button className="btn-secondary w-full justify-center">
                Export Site Map (GeoJSON)
              </button>
            </div>
          </div>

          {/* Quick Links */}
          <div className="card">
            <h3 className="font-bold mb-4">Quick Access</h3>
            <div className="space-y-2">
              <a href="/map" className="block p-3 rounded-lg bg-dark-elevated hover:bg-dark-border transition text-sm">
                <MapPin className="w-4 h-4 inline mr-2" />
                Interactive Map View
              </a>
              <a href="/" className="block p-3 rounded-lg bg-dark-elevated hover:bg-dark-border transition text-sm">
                <BarChart3 className="w-4 h-4 inline mr-2" />
                Full Data Table
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Reports
