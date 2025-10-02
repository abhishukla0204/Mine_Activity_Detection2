import { Link, useLocation } from 'react-router-dom'
import { Mountain, LayoutDashboard, Upload, Map, FileText, Activity } from 'lucide-react'

const Layout = ({ children }) => {
  const location = useLocation()

  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Analysis', path: '/analysis', icon: Activity },
    { name: 'Map View', path: '/map', icon: Map },
    { name: 'Reports', path: '/reports', icon: FileText },
    { name: 'Upload Data', path: '/upload', icon: Upload },
  ]

  const isActive = (path) => location.pathname === path

  return (
    <div className="min-h-screen bg-dark-bg">
      {/* Header */}
      <header className="glass-effect border-b border-dark-border sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-br from-primary-500 to-accent-purple p-2 rounded-lg">
                <Mountain className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold gradient-text">
                  Mining Activity Monitor
                </h1>
                <p className="text-sm text-dark-muted">
                  Automated Detection & Analysis System
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="px-4 py-2 bg-dark-elevated rounded-lg border border-dark-border">
                <span className="text-sm text-dark-muted">Status:</span>
                <span className="ml-2 text-green-400 font-semibold">● Active</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 min-h-screen bg-dark-surface border-r border-dark-border">
          <nav className="p-4 space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon
              const active = isActive(item.path)
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                    active
                      ? 'bg-gradient-to-r from-primary-500/20 to-accent-purple/20 border border-primary-500/30 text-primary-400'
                      : 'text-dark-muted hover:bg-dark-elevated hover:text-dark-text'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{item.name}</span>
                </Link>
              )
            })}
          </nav>

          {/* Sidebar Footer */}
          <div className="absolute bottom-0 w-64 p-4 border-t border-dark-border">
            <div className="card text-center">
              <p className="text-xs text-dark-muted">Version 1.0.0</p>
              <p className="text-xs text-dark-muted mt-1">© 2025 Mining Monitor</p>
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}

export default Layout
