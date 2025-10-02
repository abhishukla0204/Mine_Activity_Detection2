import { useState } from 'react'
import { motion } from 'framer-motion'
import { FileText, Download, Eye, Calendar, MapPin, BarChart3 } from 'lucide-react'

const Reports = () => {
  const [selectedReport, setSelectedReport] = useState(null)

  const reports = [
    {
      id: 1,
      title: 'Singrauli Mining Assessment - November 2024',
      date: '2024-11-15',
      type: 'comprehensive',
      region: 'Singrauli, MP',
      sites: 11,
      violations: 4,
      totalArea: 152.4,
      fileSize: '2.4 MB',
    },
    {
      id: 2,
      title: 'Quarterly Mining Report Q3 2024',
      date: '2024-09-30',
      type: 'quarterly',
      region: 'Singrauli, MP',
      sites: 11,
      violations: 3,
      totalArea: 148.2,
      fileSize: '3.1 MB',
    },
    {
      id: 3,
      title: 'Violation Alert - Unauthorized Expansion',
      date: '2024-10-22',
      type: 'alert',
      region: 'Singrauli, MP',
      sites: 2,
      violations: 2,
      totalArea: 18.5,
      fileSize: '1.2 MB',
    },
  ]

  const visualizations = [
    { name: '3D Terrain Model', type: '3d_terrain', format: 'HTML' },
    { name: 'Depth Heatmap', type: 'heatmap', format: 'PNG' },
    { name: 'Classification Map', type: 'map', format: 'HTML' },
    { name: 'Volume Analysis Chart', type: 'chart', format: 'PNG' },
  ]

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-4xl font-bold gradient-text mb-2">
          Reports & Visualizations
        </h1>
        <p className="text-dark-muted">
          Access generated reports, 3D models, and analysis results
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Reports List */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-2xl font-bold mb-4">Available Reports</h2>
          
          {reports.map((report) => (
            <motion.div
              key={report.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className={`card cursor-pointer transition-all hover:shadow-xl ${
                selectedReport?.id === report.id ? 'ring-2 ring-primary-500' : ''
              }`}
              onClick={() => setSelectedReport(report)}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <FileText className="w-5 h-5 text-primary-400" />
                    <h3 className="font-bold text-lg">{report.title}</h3>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-3 mt-4">
                    <div className="flex items-center space-x-2 text-sm">
                      <Calendar className="w-4 h-4 text-dark-muted" />
                      <span className="text-dark-muted">{report.date}</span>
                    </div>
                    <div className="flex items-center space-x-2 text-sm">
                      <MapPin className="w-4 h-4 text-dark-muted" />
                      <span className="text-dark-muted">{report.region}</span>
                    </div>
                    <div className="flex items-center space-x-2 text-sm">
                      <BarChart3 className="w-4 h-4 text-dark-muted" />
                      <span className="text-dark-muted">{report.sites} sites analyzed</span>
                    </div>
                    <div className="flex items-center space-x-2 text-sm">
                      <span className="text-dark-muted">Size: {report.fileSize}</span>
                    </div>
                  </div>

                  <div className="flex items-center space-x-3 mt-4">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        report.type === 'alert'
                          ? 'bg-red-500/20 text-red-400'
                          : report.type === 'quarterly'
                          ? 'bg-blue-500/20 text-blue-400'
                          : 'bg-purple-500/20 text-purple-400'
                      }`}
                    >
                      {report.type.toUpperCase()}
                    </span>
                    {report.violations > 0 && (
                      <span className="px-3 py-1 rounded-full text-xs font-semibold bg-red-500/20 text-red-400">
                        {report.violations} Violations
                      </span>
                    )}
                    <span className="text-sm text-dark-muted">
                      {report.totalArea} hectares
                    </span>
                  </div>
                </div>

                <div className="flex flex-col space-y-2 ml-4">
                  <button className="p-2 rounded-lg bg-primary-500/20 text-primary-400 hover:bg-primary-500/30 transition">
                    <Eye className="w-5 h-5" />
                  </button>
                  <button className="p-2 rounded-lg bg-green-500/20 text-green-400 hover:bg-green-500/30 transition">
                    <Download className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Stats */}
          <div className="card">
            <h3 className="font-bold mb-4">Report Statistics</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-dark-muted">Total Reports</span>
                <span className="font-semibold">{reports.length}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-dark-muted">Latest Report</span>
                <span className="font-semibold">Nov 2024</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-red-400">Active Violations</span>
                <span className="font-semibold">4</span>
              </div>
            </div>
          </div>

          {/* Visualizations */}
          <div className="card">
            <h3 className="font-bold mb-4">3D Visualizations</h3>
            <div className="space-y-2">
              {visualizations.map((viz, index) => (
                <button
                  key={index}
                  className="w-full p-3 rounded-lg bg-dark-elevated hover:bg-dark-border transition text-left flex items-center justify-between group"
                >
                  <div className="flex items-center space-x-3">
                    <BarChart3 className="w-4 h-4 text-primary-400" />
                    <span className="text-sm">{viz.name}</span>
                  </div>
                  <span className="text-xs text-dark-muted group-hover:text-primary-400">
                    {viz.format}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Export Options */}
          <div className="card">
            <h3 className="font-bold mb-4">Export Options</h3>
            <div className="space-y-2">
              <button className="btn-primary w-full justify-center">
                <Download className="w-4 h-4 inline mr-2" />
                Download All (ZIP)
              </button>
              <button className="btn-secondary w-full justify-center">
                Export as PDF
              </button>
              <button className="btn-secondary w-full justify-center">
                Export GeoJSON
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Report Preview */}
      {selectedReport && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
        >
          <h2 className="text-2xl font-bold mb-4">Report Preview</h2>
          <div className="bg-dark-elevated rounded-lg p-6 border border-dark-border">
            <div className="text-center text-dark-muted">
              <FileText className="w-16 h-16 mx-auto mb-4" />
              <p className="mb-4">
                Preview for: <strong>{selectedReport.title}</strong>
              </p>
              <p className="text-sm mb-6">
                Full report preview will be displayed here with embedded HTML content,
                charts, and interactive 3D visualizations.
              </p>
              <button className="btn-primary">
                Open Full Report
              </button>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  )
}

export default Reports
