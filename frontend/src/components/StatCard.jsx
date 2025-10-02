import { motion } from 'framer-motion'

const StatCard = ({ title, value, unit, icon: Icon, trend, color = 'primary' }) => {
  const colorClasses = {
    primary: 'from-primary-500 to-accent-purple',
    success: 'from-green-500 to-emerald-600',
    warning: 'from-orange-500 to-red-500',
    info: 'from-blue-500 to-cyan-500',
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="card hover:shadow-2xl transition-all duration-300 hover:scale-105"
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-dark-muted text-sm font-medium mb-2">{title}</p>
          <div className="flex items-baseline space-x-2">
            <h3 className="text-3xl font-bold text-dark-text">{value}</h3>
            {unit && <span className="text-dark-muted text-sm">{unit}</span>}
          </div>
          {trend && (
            <p className={`text-xs mt-2 ${trend > 0 ? 'text-green-400' : 'text-red-400'}`}>
              {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}% from last month
            </p>
          )}
        </div>
        <div className={`p-3 rounded-lg bg-gradient-to-br ${colorClasses[color]}`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </motion.div>
  )
}

export default StatCard
