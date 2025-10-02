import { useState } from 'react'
import { MapContainer, TileLayer, Polygon, Popup, Marker } from 'react-leaflet'
import { motion } from 'framer-motion'
import { MapPin, AlertTriangle, CheckCircle, Info } from 'lucide-react'
import 'leaflet/dist/leaflet.css'

const MapView = () => {
  const [selectedMine, setSelectedMine] = useState(null)
  const [showLegal, setShowLegal] = useState(true)
  const [showIllegal, setShowIllegal] = useState(true)

  // Singrauli coordinates (approximate)
  const center = [24.2, 82.7]

  // Mock mining data with coordinates
  const miningAreas = [
    {
      id: 1,
      name: 'Mine Site 1',
      type: 'legal',
      area: 15.2,
      depth: 28,
      volume: 425000,
      coordinates: [[24.21, 82.71], [24.22, 82.71], [24.22, 82.72], [24.21, 82.72]],
    },
    {
      id: 2,
      name: 'Mine Site 2',
      type: 'illegal',
      area: 8.5,
      depth: 18,
      volume: 153000,
      coordinates: [[24.19, 82.73], [24.20, 82.73], [24.20, 82.74], [24.19, 82.74]],
    },
    {
      id: 3,
      name: 'Mine Site 3',
      type: 'legal',
      area: 22.8,
      depth: 35,
      volume: 798000,
      coordinates: [[24.23, 82.69], [24.24, 82.69], [24.24, 82.70], [24.23, 82.70]],
    },
    {
      id: 4,
      name: 'Mine Site 4',
      type: 'illegal',
      area: 12.3,
      depth: 22,
      volume: 270600,
      coordinates: [[24.18, 82.68], [24.19, 82.68], [24.19, 82.69], [24.18, 82.69]],
    },
  ]

  const getPolygonColor = (type) => {
    return type === 'legal' ? '#10b981' : '#ef4444'
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold gradient-text mb-2">
            Interactive Map View
          </h1>
          <p className="text-dark-muted">
            Geospatial visualization of detected mining areas
          </p>
        </div>

        {/* Map Controls */}
        <div className="flex space-x-3">
          <button
            onClick={() => setShowLegal(!showLegal)}
            className={`px-4 py-2 rounded-lg border transition ${
              showLegal
                ? 'bg-green-500/20 border-green-500 text-green-400'
                : 'bg-dark-elevated border-dark-border text-dark-muted'
            }`}
          >
            <CheckCircle className="w-4 h-4 inline mr-2" />
            Legal Sites
          </button>
          <button
            onClick={() => setShowIllegal(!showIllegal)}
            className={`px-4 py-2 rounded-lg border transition ${
              showIllegal
                ? 'bg-red-500/20 border-red-500 text-red-400'
                : 'bg-dark-elevated border-dark-border text-dark-muted'
            }`}
          >
            <AlertTriangle className="w-4 h-4 inline mr-2" />
            Illegal Sites
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Map Container */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="lg:col-span-2 card p-0 overflow-hidden h-[600px]"
        >
          <MapContainer
            center={center}
            zoom={12}
            style={{ height: '100%', width: '100%' }}
            className="rounded-xl"
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {miningAreas.map((mine) => {
              if (mine.type === 'legal' && !showLegal) return null
              if (mine.type === 'illegal' && !showIllegal) return null

              return (
                <Polygon
                  key={mine.id}
                  positions={mine.coordinates}
                  pathOptions={{
                    color: getPolygonColor(mine.type),
                    fillColor: getPolygonColor(mine.type),
                    fillOpacity: 0.3,
                    weight: 2,
                  }}
                  eventHandlers={{
                    click: () => setSelectedMine(mine),
                  }}
                >
                  <Popup>
                    <div className="p-2">
                      <h3 className="font-bold mb-2">{mine.name}</h3>
                      <div className="space-y-1 text-sm">
                        <p>
                          <strong>Status:</strong>{' '}
                          <span
                            className={
                              mine.type === 'legal' ? 'text-green-600' : 'text-red-600'
                            }
                          >
                            {mine.type === 'legal' ? 'Legal' : 'Illegal'}
                          </span>
                        </p>
                        <p>
                          <strong>Area:</strong> {mine.area} hectares
                        </p>
                        <p>
                          <strong>Depth:</strong> {mine.depth}m
                        </p>
                        <p>
                          <strong>Volume:</strong> {mine.volume.toLocaleString()} m³
                        </p>
                      </div>
                    </div>
                  </Popup>
                </Polygon>
              )
            })}
          </MapContainer>
        </motion.div>

        {/* Mine Details Sidebar */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="space-y-6"
        >
          {/* Selected Mine Details */}
          {selectedMine ? (
            <div className="card">
              <div className="flex items-start justify-between mb-4">
                <h3 className="font-bold text-lg">{selectedMine.name}</h3>
                <span
                  className={`px-3 py-1 rounded-full text-sm ${
                    selectedMine.type === 'legal'
                      ? 'bg-green-500/20 text-green-400'
                      : 'bg-red-500/20 text-red-400'
                  }`}
                >
                  {selectedMine.type === 'legal' ? 'Legal' : 'Illegal'}
                </span>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between items-center p-3 bg-dark-elevated rounded-lg">
                  <span className="text-dark-muted">Area</span>
                  <span className="font-semibold">{selectedMine.area} ha</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-dark-elevated rounded-lg">
                  <span className="text-dark-muted">Average Depth</span>
                  <span className="font-semibold">{selectedMine.depth} m</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-dark-elevated rounded-lg">
                  <span className="text-dark-muted">Excavation Volume</span>
                  <span className="font-semibold">
                    {selectedMine.volume.toLocaleString()} m³
                  </span>
                </div>
              </div>

              <button className="btn-primary w-full mt-4">
                View Detailed Report
              </button>
            </div>
          ) : (
            <div className="card text-center">
              <MapPin className="w-12 h-12 mx-auto mb-4 text-dark-muted" />
              <p className="text-dark-muted">
                Click on a mining area to view details
              </p>
            </div>
          )}

          {/* Statistics */}
          <div className="card">
            <h3 className="font-bold mb-4">Map Statistics</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-dark-muted">Total Sites</span>
                <span className="font-semibold">{miningAreas.length}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-green-400">Legal Sites</span>
                <span className="font-semibold">
                  {miningAreas.filter((m) => m.type === 'legal').length}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-red-400">Illegal Sites</span>
                <span className="font-semibold">
                  {miningAreas.filter((m) => m.type === 'illegal').length}
                </span>
              </div>
            </div>
          </div>

          {/* Legend */}
          <div className="card">
            <h3 className="font-bold mb-4">Legend</h3>
            <div className="space-y-2">
              <div className="flex items-center space-x-3">
                <div className="w-6 h-6 bg-green-500 rounded border-2 border-green-600" />
                <span className="text-sm">Legal Mining Area</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-6 h-6 bg-red-500 rounded border-2 border-red-600" />
                <span className="text-sm">Illegal Mining Area</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-6 h-6 bg-yellow-500 rounded border-2 border-yellow-600" />
                <span className="text-sm">Authorized Boundary</span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default MapView
