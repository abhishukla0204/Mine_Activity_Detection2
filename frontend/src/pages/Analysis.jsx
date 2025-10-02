import { useState } from 'react'
import { motion } from 'framer-motion'
import { Play, Activity, TrendingUp, Pause, RefreshCw } from 'lucide-react'

const Analysis = () => {
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [progress, setProgress] = useState(0)

  const handleStartAnalysis = () => {
    setIsAnalyzing(true)
    setProgress(0)
    
    // Simulate progress
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          setIsAnalyzing(false)
          return 100
        }
        return prev + 10
      })
    }, 500)
  }

  const analysisSteps = [
    { name: 'Loading Data', status: progress > 0 ? 'completed' : 'pending' },
    { name: 'Detecting Mining Areas', status: progress > 20 ? 'completed' : progress > 0 ? 'processing' : 'pending' },
    { name: 'Boundary Analysis', status: progress > 40 ? 'completed' : progress > 20 ? 'processing' : 'pending' },
    { name: 'Depth Calculation', status: progress > 60 ? 'completed' : progress > 40 ? 'processing' : 'pending' },
    { name: 'Volume Estimation', status: progress > 80 ? 'completed' : progress > 60 ? 'processing' : 'pending' },
    { name: 'Generating Reports', status: progress === 100 ? 'completed' : progress > 80 ? 'processing' : 'pending' },
  ]

  return (
    <div className="space-y-8 animate-fade-in">
      <div>
        <h1 className="text-4xl font-bold gradient-text mb-2">
          Real-time Analysis
        </h1>
        <p className="text-dark-muted">
          Monitor mining detection and analysis progress
        </p>
      </div>

      {/* Control Panel */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold">Analysis Control</h3>
          <div className="flex space-x-3">
            <button
              onClick={handleStartAnalysis}
              disabled={isAnalyzing}
              className="btn-primary disabled:opacity-50"
            >
              {isAnalyzing ? (
                <>
                  <Pause className="w-5 h-5 inline mr-2" />
                  Running...
                </>
              ) : (
                <>
                  <Play className="w-5 h-5 inline mr-2" />
                  Start Analysis
                </>
              )}
            </button>
            <button className="btn-secondary">
              <RefreshCw className="w-5 h-5 inline mr-2" />
              Reset
            </button>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-dark-muted">Overall Progress</span>
            <span className="text-sm font-semibold">{progress}%</span>
          </div>
          <div className="w-full bg-dark-elevated rounded-full h-3">
            <motion.div
              className="h-3 rounded-full bg-gradient-to-r from-primary-500 to-accent-purple"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>
        </div>

        {/* Analysis Steps */}
        <div className="space-y-3">
          {analysisSteps.map((step, index) => (
            <motion.div
              key={step.name}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`p-4 rounded-lg flex items-center justify-between ${
                step.status === 'completed'
                  ? 'bg-green-500/10 border border-green-500/30'
                  : step.status === 'processing'
                  ? 'bg-primary-500/10 border border-primary-500/30 animate-pulse'
                  : 'bg-dark-elevated border border-dark-border'
              }`}
            >
              <div className="flex items-center space-x-3">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    step.status === 'completed'
                      ? 'bg-green-500'
                      : step.status === 'processing'
                      ? 'bg-primary-500 animate-pulse'
                      : 'bg-dark-border'
                  }`}
                >
                  {step.status === 'completed' && '✓'}
                  {step.status === 'processing' && <Activity className="w-4 h-4 animate-spin" />}
                  {step.status === 'pending' && index + 1}
                </div>
                <span className="font-medium">{step.name}</span>
              </div>
              <span
                className={`text-sm px-3 py-1 rounded-full ${
                  step.status === 'completed'
                    ? 'bg-green-500/20 text-green-400'
                    : step.status === 'processing'
                    ? 'bg-primary-500/20 text-primary-400'
                    : 'bg-dark-border text-dark-muted'
                }`}
              >
                {step.status === 'completed' ? 'Completed' : step.status === 'processing' ? 'Processing...' : 'Pending'}
              </span>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Live Results */}
      {progress > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          <div className="card">
            <h4 className="font-bold mb-2">Sites Detected</h4>
            <p className="text-3xl font-bold gradient-text">
              {Math.floor((progress / 100) * 11)}
            </p>
            <p className="text-sm text-dark-muted mt-2">
              <TrendingUp className="w-4 h-4 inline text-green-400" /> Mining areas found
            </p>
          </div>

          <div className="card">
            <h4 className="font-bold mb-2">Data Processed</h4>
            <p className="text-3xl font-bold gradient-text">
              {Math.floor((progress / 100) * 152)} <span className="text-lg">ha</span>
            </p>
            <p className="text-sm text-dark-muted mt-2">Total area analyzed</p>
          </div>

          <div className="card">
            <h4 className="font-bold mb-2">Time Elapsed</h4>
            <p className="text-3xl font-bold gradient-text">
              {Math.floor((progress / 100) * 45)} <span className="text-lg">sec</span>
            </p>
            <p className="text-sm text-dark-muted mt-2">Processing time</p>
          </div>
        </motion.div>
      )}

      {/* Completion Message */}
      {progress === 100 && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="card bg-green-500/10 border-green-500/30"
        >
          <div className="text-center">
            <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <Activity className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-2xl font-bold text-green-400 mb-2">
              Analysis Complete!
            </h3>
            <p className="text-dark-muted mb-6">
              Successfully analyzed 11 mining sites. View detailed reports and visualizations.
            </p>
            <div className="flex justify-center space-x-4">
              <button className="btn-primary">View Dashboard</button>
              <button className="btn-secondary">Download Report</button>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  )
}

export default Analysis
