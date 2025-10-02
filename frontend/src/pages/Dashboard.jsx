import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import StatCard from '../components/StatCard'
import AreaChart from '../components/AreaChart'
import { 
  Mountain, AlertTriangle, TrendingUp, Layers, 
  BarChart3, Activity, MapPin, FileWarning 
} from 'lucide-react'

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalArea: 152.4,
    legalArea: 98.6,
    illegalArea: 53.8,
    totalSites: 11,
    violations: 4,
    avgDepth: 24.5,
    totalVolume: 3450000,
    illegalPercentage: 35.3
  })

  const [recentAnalysis, setRecentAnalysis] = useState([
    { id: 1, name: 'Singrauli Analysis', date: '2025-10-02', status: 'completed', sites: 11 },
    { id: 2, name: 'Jharkhand Survey', date: '2025-09-28', status: 'completed', sites: 8 },
    { id: 3, name: 'Chhattisgarh Scan', date: '2025-09-20', status: 'completed', sites: 6 },
  ])

  // Chart data for mining activity over time
  const chartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
    datasets: [
      {
        label: 'Legal Mining (hectares)',
        data: [85, 88, 92, 90, 93, 95, 96, 97, 98, 98.6],
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        fill: true,
        tension: 0.4,
      },
      {
        label: 'Illegal Mining (hectares)',
        data: [12, 15, 18, 22, 28, 35, 42, 46, 50, 53.8],
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        fill: true,
        tension: 0.4,
      },
    ],
  }

  const depthData = {
    labels: ['Mine 1', 'Mine 2', 'Mine 3', 'Mine 4', 'Mine 5', 'Mine 6', 'Mine 7', 'Mine 8'],
    datasets: [
      {
        label: 'Average Depth (meters)',
        data: [18, 22, 35, 28, 42, 25, 31, 38],
        borderColor: '#667eea',
        backgroundColor: 'rgba(102, 126, 234, 0.1)',
        fill: true,
        tension: 0.4,
      },
    ],
  }

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold gradient-text mb-2">
            Mining Activity Dashboard
          </h1>
          <p className="text-dark-muted">
            Real-time monitoring and analysis of mining activities
          </p>
        </div>
        <button className="btn-primary">
          <Activity className="w-5 h-5 inline mr-2" />
          Run New Analysis
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Mining Area"
          value={stats.totalArea}
          unit="hectares"
          icon={Mountain}
          trend={8.3}
          color="info"
        />
        <StatCard
          title="Legal Mining"
          value={stats.legalArea}
          unit="hectares"
          icon={TrendingUp}
          trend={5.2}
          color="success"
        />
        <StatCard
          title="Illegal Mining"
          value={stats.illegalArea}
          unit="hectares"
          icon={AlertTriangle}
          trend={12.8}
          color="warning"
        />
        <StatCard
          title="Active Sites"
          value={stats.totalSites}
          unit="sites"
          icon={MapPin}
          color="primary"
        />
      </div>

      {/* Secondary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Violations Detected"
          value={stats.violations}
          unit="high severity"
          icon={FileWarning}
          color="warning"
        />
        <StatCard
          title="Average Depth"
          value={stats.avgDepth}
          unit="meters"
          icon={Layers}
          color="info"
        />
        <StatCard
          title="Total Volume"
          value={(stats.totalVolume / 1000000).toFixed(2)}
          unit="million m³"
          icon={BarChart3}
          color="primary"
        />
        <StatCard
          title="Illegal Activity"
          value={stats.illegalPercentage}
          unit="% of total"
          icon={AlertTriangle}
          trend={-3.2}
          color="warning"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="card h-96"
        >
          <AreaChart 
            data={chartData} 
            title="Mining Activity Trend (2025)"
          />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="card h-96"
        >
          <AreaChart 
            data={depthData} 
            title="Mining Depth Analysis"
          />
        </motion.div>
      </div>

      {/* Violations Alert */}
      {stats.violations > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="card bg-gradient-to-r from-red-500/10 to-orange-500/10 border-red-500/30"
        >
          <div className="flex items-start space-x-4">
            <div className="p-3 bg-red-500/20 rounded-lg">
              <AlertTriangle className="w-6 h-6 text-red-400" />
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-red-400 mb-2">
                ⚠️ {stats.violations} Violations Detected
              </h3>
              <p className="text-dark-muted mb-4">
                Illegal mining activities detected outside authorized boundaries. 
                Immediate action required for {stats.illegalArea} hectares of unauthorized excavation.
              </p>
              <div className="flex space-x-4">
                <button className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition">
                  View Detailed Report
                </button>
                <button className="px-4 py-2 bg-dark-elevated border border-dark-border rounded-lg hover:bg-dark-surface transition">
                  Export Violation Data
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Recent Analysis */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.5 }}
        className="card"
      >
        <h3 className="text-xl font-bold mb-4">Recent Analysis</h3>
        <div className="space-y-3">
          {recentAnalysis.map((analysis) => (
            <div
              key={analysis.id}
              className="flex items-center justify-between p-4 bg-dark-elevated rounded-lg hover:bg-dark-surface transition cursor-pointer"
            >
              <div className="flex items-center space-x-4">
                <div className="p-2 bg-primary-500/20 rounded-lg">
                  <Activity className="w-5 h-5 text-primary-400" />
                </div>
                <div>
                  <h4 className="font-semibold">{analysis.name}</h4>
                  <p className="text-sm text-dark-muted">
                    {analysis.date} • {analysis.sites} sites detected
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm">
                  {analysis.status}
                </span>
                <button className="text-primary-400 hover:text-primary-300 transition">
                  View →
                </button>
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.6 }}
          className="card hover:shadow-2xl transition cursor-pointer"
        >
          <div className="text-center">
            <div className="inline-block p-4 bg-gradient-to-br from-primary-500 to-accent-purple rounded-lg mb-4">
              <Activity className="w-8 h-8 text-white" />
            </div>
            <h4 className="font-bold mb-2">Start Analysis</h4>
            <p className="text-sm text-dark-muted">
              Upload new satellite data and run mining detection
            </p>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.7 }}
          className="card hover:shadow-2xl transition cursor-pointer"
        >
          <div className="text-center">
            <div className="inline-block p-4 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg mb-4">
              <MapPin className="w-8 h-8 text-white" />
            </div>
            <h4 className="font-bold mb-2">View Map</h4>
            <p className="text-sm text-dark-muted">
              Interactive map with all detected mining areas
            </p>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.8 }}
          className="card hover:shadow-2xl transition cursor-pointer"
        >
          <div className="text-center">
            <div className="inline-block p-4 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg mb-4">
              <FileWarning className="w-8 h-8 text-white" />
            </div>
            <h4 className="font-bold mb-2">Generate Report</h4>
            <p className="text-sm text-dark-muted">
              Create comprehensive analysis report
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Dashboard
