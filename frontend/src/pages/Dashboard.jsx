import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import StatCard from '../components/StatCard'
import { 
  Mountain, AlertTriangle, TrendingUp, Layers, 
  MapPin, BarChart3
} from 'lucide-react'

const Dashboard = () => {
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
          <Mountain className="w-12 h-12 mx-auto mb-4 text-primary-400 animate-pulse" />
          <p className="text-dark-muted">Loading mining data...</p>
        </div>
      </div>
    )
  }

  const { metadata, mines } = miningData

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold gradient-text mb-2">
            Mining Monitoring Overview
          </h1>
          <p className="text-dark-muted">
            Singrauli region - Real-time satellite imagery analysis
          </p>
        </div>
        <Link to="/map" className="btn-primary">
          <MapPin className="w-5 h-5 inline mr-2" />
          View Interactive Map
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Mining Sites"
          value={metadata.total_mines}
          unit="sites"
          icon={Mountain}
          color="info"
        />
        <StatCard
          title="Authorized Sites"
          value={metadata.legal_mines}
          unit="sites"
          icon={TrendingUp}
          color="success"
        />
        <StatCard
          title="Unauthorized Sites"
          value={metadata.illegal_mines}
          unit="sites"
          icon={AlertTriangle}
          color="danger"
        />
        <StatCard
          title="Total Area"
          value={(metadata.total_area_hectares / 1000).toFixed(2)}
          unit="km²"
          icon={Layers}
          color="info"
        />
      </div>

      {/* Mining Sites Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Area Distribution */}
        <div className="card">
          <h3 className="text-xl font-bold mb-6 flex items-center">
            <BarChart3 className="w-6 h-6 mr-2 text-primary-400" />
            Area Distribution
          </h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-dark-muted">Authorized Mining</span>
                <span className="font-bold text-green-400">
                  {(metadata.legal_area_hectares / 1000).toFixed(2)} km²
                </span>
              </div>
              <div className="w-full bg-dark-elevated rounded-full h-3">
                <div
                  className="h-3 rounded-full bg-green-500"
                  style={{ width: `${(metadata.legal_area_hectares / metadata.total_area_hectares) * 100}%` }}
                />
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-dark-muted">Unauthorized Mining</span>
                <span className="font-bold text-red-400">
                  {(metadata.illegal_area_hectares / 1000).toFixed(2)} km²
                </span>
              </div>
              <div className="w-full bg-dark-elevated rounded-full h-3">
                <div
                  className="h-3 rounded-full bg-red-500"
                  style={{ width: `${(metadata.illegal_area_hectares / metadata.total_area_hectares) * 100}%` }}
                />
              </div>
            </div>
          </div>
          <div className="mt-6 p-4 bg-dark-elevated rounded-lg">
            <p className="text-sm text-dark-muted mb-2">Compliance Rate</p>
            <p className="text-3xl font-bold gradient-text">
              {((metadata.legal_area_hectares / metadata.total_area_hectares) * 100).toFixed(1)}%
            </p>
          </div>
        </div>

        {/* Volume Metrics */}
        <div className="card">
          <h3 className="text-xl font-bold mb-6 flex items-center">
            <Mountain className="w-6 h-6 mr-2 text-primary-400" />
            Excavation Summary
          </h3>
          <div className="space-y-4">
            <div className="p-4 bg-dark-elevated rounded-xl">
              <p className="text-sm text-dark-muted mb-2">Total Excavation Volume</p>
              <p className="text-3xl font-bold gradient-text">
                {(metadata.total_volume_m3 / 1000000000).toFixed(2)} B m³
              </p>
            </div>
            <div className="p-4 bg-dark-elevated rounded-xl">
              <p className="text-sm text-dark-muted mb-2">Average Depth</p>
              <p className="text-3xl font-bold gradient-text">
                {(mines.reduce((sum, m) => sum + (m.depth_m || 0), 0) / mines.length).toFixed(1)} m
              </p>
            </div>
            <div className="p-4 bg-dark-elevated rounded-xl">
              <p className="text-sm text-dark-muted mb-2">Data Source</p>
              <p className="text-sm font-medium">{metadata.data_source}</p>
              <p className="text-xs text-dark-muted mt-1">
                Last updated: {metadata.computation_date}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Mine Sites Table */}
      <div className="card">
        <h3 className="text-xl font-bold mb-6">Mining Sites</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-dark-border">
                <th className="text-left py-3 px-4">Site ID</th>
                <th className="text-left py-3 px-4">Status</th>
                <th className="text-right py-3 px-4">Area (ha)</th>
                <th className="text-right py-3 px-4">Depth (m)</th>
                <th className="text-right py-3 px-4">Volume (M m³)</th>
                <th className="text-left py-3 px-4">Operator</th>
              </tr>
            </thead>
            <tbody>
              {mines.map((mine) => (
                <motion.tr
                  key={mine.id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="border-b border-dark-border/50 hover:bg-dark-elevated transition"
                >
                  <td className="py-3 px-4 font-medium">Site #{mine.id}</td>
                  <td className="py-3 px-4">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        mine.type === 'legal'
                          ? 'bg-green-500/20 text-green-400'
                          : 'bg-red-500/20 text-red-400'
                      }`}
                    >
                      {mine.type === 'legal' ? 'Authorized' : 'Unauthorized'}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right">{mine.area_hectares.toFixed(1)}</td>
                  <td className="py-3 px-4 text-right">{mine.depth_m.toFixed(0)}</td>
                  <td className="py-3 px-4 text-right">
                    {(mine.volume_m3 / 1000000).toFixed(1)}
                  </td>
                  <td className="py-3 px-4 text-sm text-dark-muted">{mine.operator}</td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Link to="/map" className="card hover:ring-2 hover:ring-primary-500 transition cursor-pointer">
          <MapPin className="w-12 h-12 text-primary-400 mb-4" />
          <h4 className="font-bold mb-2 text-lg">Interactive Map</h4>
          <p className="text-sm text-dark-muted">
            View satellite imagery with site boundaries and detailed information
          </p>
        </Link>

        <Link to="/reports" className="card hover:ring-2 hover:ring-primary-500 transition cursor-pointer">
          <BarChart3 className="w-12 h-12 text-accent-purple mb-4" />
          <h4 className="font-bold mb-2 text-lg">Analysis Reports</h4>
          <p className="text-sm text-dark-muted">
            Access detailed reports and compliance documentation
          </p>
        </Link>
      </div>
    </div>
  )
}

export default Dashboard
