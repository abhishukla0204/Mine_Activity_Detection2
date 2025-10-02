import { useState, useEffect } from 'react'
import { MapContainer, ImageOverlay, Polygon, useMap } from 'react-leaflet'
import L from 'leaflet'
import { motion, AnimatePresence } from 'framer-motion'
import { MapPin, AlertTriangle, CheckCircle, Layers, TrendingUp, TrendingDown, Activity } from 'lucide-react'
import 'leaflet/dist/leaflet.css'

// Component to disable map interactions
const DisableMapInteraction = () => {
  const map = useMap()
  
  useEffect(() => {
    try {
      // Disable all map interactions
      if (map.dragging) map.dragging.disable()
      if (map.touchZoom) map.touchZoom.disable()
      if (map.doubleClickZoom) map.doubleClickZoom.disable()
      if (map.scrollWheelZoom) map.scrollWheelZoom.disable()
      if (map.boxZoom) map.boxZoom.disable()
      if (map.keyboard) map.keyboard.disable()
      if (map.tap) map.tap.disable()
    } catch (error) {
      console.error('Error disabling map interactions:', error)
    }
  }, [map])
  
  return null
}

const MapView = () => {
  const [selectedMine, setSelectedMine] = useState(null)
  const [showLegal, setShowLegal] = useState(true)
  const [showIllegal, setShowIllegal] = useState(true)
  const [hoveredMine, setHoveredMine] = useState(null)
  const [mapError, setMapError] = useState(false)
  const [miningAreas, setMiningAreas] = useState([])

  // Image dimensions from your satellite image
  const imageWidth = 1500
  const imageHeight = 719
  
  // Calculate aspect ratio
  const aspectRatio = imageWidth / imageHeight  // 2.086:1
  
  // Use pixel coordinate system matching the image dimensions
  // This preserves the original aspect ratio and dimensions
  // In Leaflet's Simple CRS, coordinates are [y, x] where y=0 is top
  const imageBounds = [
    [0, 0],                           // Top-left corner
    [imageHeight, imageWidth]         // Bottom-right corner
  ]
  
  // Center of the image in pixel coordinates [y, x]
  const center = [imageHeight / 2, imageWidth / 2]
  
  // Path to satellite image
  const satelliteImageUrl = '/singrauli_satellite.jpg'

  // Load actual mine boundaries from COCO annotations
  useEffect(() => {
    // Try to load computed metrics first, fall back to raw annotations
    fetch('/computed_metrics.json?t=' + Date.now())  // Cache busting
      .then(res => {
        if (!res.ok) throw new Error('Computed metrics not found')
        return res.json()
      })
      .then(data => {
        // Use pre-computed metrics
        console.log('✓ Loaded computed metrics:', data.metadata)
        console.log('✓ First mine coordinates sample:', data.mines[0]?.coordinates?.slice(0, 3))
        console.log('✓ First mine name:', data.mines[0]?.name)
        console.log('✓ Total mines loaded:', data.mines.length)
        
        // Verify coordinates are in [y, x] format
        if (data.mines[0]?.coordinates) {
          const firstCoord = data.mines[0].coordinates[0]
          console.log('✓ First coordinate [y, x]:', firstCoord, 
                      '(should be y < 719, x < 1500)')
        }
        
        setMiningAreas(data.mines)
      })
      .catch(err => {
        console.log('Computed metrics not available, loading raw annotations...')
        // Fall back to raw COCO annotations
        return fetch('/mine_annotations.json')
          .then(res => res.json())
          .then(data => {
            const areas = data.annotations.map((ann, idx) => {
              // Convert COCO segmentation (pixel coordinates) to map coordinates
              const segmentation = ann.segmentation[0]
              const coordinates = []
              
              for (let i = 0; i < segmentation.length; i += 2) {
                const x = segmentation[i]
                const y = segmentation[i + 1]
                
                // Convert pixel coords to Leaflet Simple CRS coordinates [y, x]
                coordinates.push([y, x])
              }
              
              // Get category name
              const category = data.categories.find(cat => cat.id === ann.category_id)
              const mineName = category ? category.name : `Mine ${idx + 1}`
              
              // Assign legal/illegal status (you can customize this logic)
              const isLegal = idx < 7 // First 7 legal, rest illegal
              
              return {
                id: idx + 1,
                name: mineName.charAt(0).toUpperCase() + mineName.slice(1),
                type: isLegal ? 'legal' : 'illegal',
                area: (ann.area / 10000).toFixed(1), // Rough estimate in hectares
                depth: (Math.random() * 20 + 20).toFixed(1),
                volume: Math.floor(ann.area * (Math.random() * 20 + 20)),
                avgElevation: Math.floor(Math.random() * 30 + 270),
                perimeter: (Math.sqrt(ann.area) * 4 / 1000).toFixed(2),
                material: 'Coal',
                operator: isLegal ? 'NCL' : 'Unauthorized',
                lastInspection: isLegal ? '2024-09-' + (10 + idx) : 'N/A',
                compliance: isLegal ? Math.floor(Math.random() * 10 + 90) : Math.floor(Math.random() * 30 + 30),
                coordinates: coordinates,
              }
            })
            
            setMiningAreas(areas)
          })
      })
      .catch(err => {
        console.error('Error loading mine data:', err)
        setMiningAreas([])
      })
  }, [])

  const getPolygonColor = (type) => {
    return type === 'legal' ? '#10b981' : '#ef4444'
  }

  const getPolygonStyle = (mine, isHovered) => {
    const baseColor = getPolygonColor(mine.type)
    return {
      color: baseColor,
      fillColor: baseColor,
      fillOpacity: isHovered ? 0.6 : 0.4,
      weight: isHovered ? 3 : 2,
    }
  }

  const filteredMines = miningAreas.filter(mine => {
    if (mine.type === 'legal' && !showLegal) return false
    if (mine.type === 'illegal' && !showIllegal) return false
    return true
  })

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold gradient-text mb-2">
            Interactive Mining Map
          </h1>
          <p className="text-dark-muted">
            Monitoring {miningAreas.length} mining sites in Singrauli region with real-time satellite imagery analysis
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
            Legal ({miningAreas.filter(m => m.type === 'legal').length})
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
            Illegal ({miningAreas.filter(m => m.type === 'illegal').length})
          </button>
        </div>
      </div>

      {/* Main Content Grid - Map on left, Stats on right */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6">
        {/* Map Container - Takes 3 columns */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="lg:col-span-3 card p-0 overflow-hidden relative"
          style={{ 
            aspectRatio: `${imageWidth} / ${imageHeight}`,
            width: '100%',
            maxWidth: '100%',
            minHeight: '600px'
          }}
        >
        {mapError ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <AlertTriangle className="w-16 h-16 mx-auto mb-4 text-red-400" />
              <h3 className="font-bold mb-2">Map Loading Error</h3>
              <p className="text-dark-muted text-sm mb-4">
                Unable to load the map. Please refresh the page.
              </p>
              <button 
                onClick={() => window.location.reload()} 
                className="btn-primary"
              >
                Refresh Page
              </button>
            </div>
          </div>
        ) : (
          <MapContainer
              center={center}
              zoom={-1}
              minZoom={-2}
              maxZoom={2}
              crs={L.CRS.Simple}
              maxBounds={imageBounds}
              maxBoundsViscosity={1.0}
              style={{ height: '100%', width: '100%', cursor: 'pointer', backgroundColor: '#1a1a2e' }}
              className="rounded-xl"
              zoomControl={false}
              scrollWheelZoom={false}
              doubleClickZoom={false}
              dragging={false}
              attributionControl={false}
              whenCreated={(map) => {
                // Map successfully created
                console.log('Map loaded successfully')
                console.log('Image bounds:', imageBounds)
                console.log('Map container size:', map.getSize())
                // Force the map to show the entire image without cropping
                setTimeout(() => {
                  map.fitBounds(imageBounds, { 
                    padding: [0, 0], 
                    animate: false,
                    maxZoom: 0
                  })
                }, 100)
              }}
            >
              <DisableMapInteraction />
              
              {/* Use satellite image as base layer instead of OpenStreetMap */}
              <ImageOverlay
                url={satelliteImageUrl}
                bounds={imageBounds}
                opacity={1}
                zIndex={1}
              />

              {/* Debug markers at corners to verify coordinate system */}
              {process.env.NODE_ENV === 'development' && (
                <>
                  {/* Top-left corner marker */}
                  <Polygon
                    positions={[[0, 0], [10, 0], [10, 10], [0, 10]]}
                    pathOptions={{ color: 'yellow', fillColor: 'yellow', fillOpacity: 0.8 }}
                  />
                  {/* Bottom-right corner marker */}
                  <Polygon
                    positions={[[imageHeight-10, imageWidth-10], [imageHeight, imageWidth-10], 
                                [imageHeight, imageWidth], [imageHeight-10, imageWidth]]}
                    pathOptions={{ color: 'cyan', fillColor: 'cyan', fillOpacity: 0.8 }}
                  />
                </>
              )}

              {filteredMines.map((mine) => (
                <Polygon
                  key={mine.id}
                  positions={mine.coordinates}
                  pathOptions={getPolygonStyle(mine, hoveredMine === mine.id)}
                  eventHandlers={{
                    click: () => setSelectedMine(mine),
                    mouseover: () => setHoveredMine(mine.id),
                    mouseout: () => setHoveredMine(null),
                  }}
                />
              ))}
            </MapContainer>
          )}

          {/* Hover Tooltip */}
          <AnimatePresence>
            {hoveredMine && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
                className="absolute top-4 left-4 bg-dark-surface/95 backdrop-blur-sm border border-dark-border rounded-lg p-3 pointer-events-none z-[1000]"
              >
                <p className="text-sm font-semibold">
                  Mining Site #{miningAreas.find(m => m.id === hoveredMine)?.id}
                </p>
                <p className="text-xs text-dark-muted mt-1">
                  {miningAreas.find(m => m.id === hoveredMine)?.area_hectares?.toFixed(1) || 
                   miningAreas.find(m => m.id === hoveredMine)?.area} ha
                  {' • '}
                  Click for details
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>

        {/* Statistics Sidebar - Takes 1 column on the right */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="space-y-6"
        >
          {/* Quick Statistics */}
          <div className="card p-6">
            <h3 className="font-bold text-lg mb-6 flex items-center">
              <Activity className="w-6 h-6 mr-2 text-primary-400" />
              Statistics
            </h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center p-3 bg-dark-elevated rounded-lg">
                <span className="text-dark-muted text-sm">Total Sites</span>
                <span className="font-bold text-xl">{miningAreas.length}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-green-500/10 rounded-lg border border-green-500/20">
                <span className="text-green-400 font-medium text-sm">Legal</span>
                <span className="font-bold text-xl text-green-400">
                  {miningAreas.filter((m) => m.type === 'legal').length}
                </span>
              </div>
              <div className="flex justify-between items-center p-3 bg-red-500/10 rounded-lg border border-red-500/20">
                <span className="text-red-400 font-medium text-sm">Illegal</span>
                <span className="font-bold text-xl text-red-400">
                  {miningAreas.filter((m) => m.type === 'illegal').length}
                </span>
              </div>
              <div className="border-t border-dark-border pt-4 mt-4 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-dark-muted text-sm">Total Area</span>
                  <span className="font-bold">
                    {miningAreas.reduce((sum, m) => sum + (m.area_hectares || m.area || 0), 0).toFixed(0)} ha
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-dark-muted text-sm">Volume</span>
                  <span className="font-bold">
                    {(miningAreas.reduce((sum, m) => sum + (m.volume_m3 || m.volume || 0), 0) / 1000000).toFixed(1)}M m³
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Legend Card */}
          <div className="card p-6">
            <h3 className="font-bold text-lg mb-4 flex items-center">
              <Layers className="w-5 h-5 mr-2 text-primary-400" />
              Map Legend
            </h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-5 bg-green-500 rounded border-2 border-green-600" />
                <div>
                  <span className="text-sm font-medium block">Authorized Sites</span>
                  <span className="text-xs text-dark-muted">Licensed mining operations</span>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-8 h-5 bg-red-500 rounded border-2 border-red-600" />
                <div>
                  <span className="text-sm font-medium block">Unauthorized Sites</span>
                  <span className="text-xs text-dark-muted">Illegal excavation detected</span>
                </div>
              </div>
            </div>
            <div className="mt-4 pt-3 border-t border-dark-border">
              <p className="text-xs text-dark-muted flex items-center">
                <MapPin className="w-3 h-3 mr-1" />
                Click any site to view details
              </p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Sliding Mine Details Panel from Right */}
      <AnimatePresence>
        {selectedMine && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[2000]"
              onClick={() => setSelectedMine(null)}
            />
            
            {/* Sliding Panel */}
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="fixed top-0 right-0 h-full w-full md:w-[500px] bg-dark-surface border-l border-dark-border z-[2001] overflow-y-auto shadow-2xl"
            >
              {/* Panel Header */}
              <div className="sticky top-0 bg-dark-surface/95 backdrop-blur-sm border-b border-dark-border p-6 z-10">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h2 className="font-bold text-2xl mb-2">Mining Site #{selectedMine.id}</h2>
                    <p className="text-sm text-dark-muted">{selectedMine.operator}</p>
                  </div>
                  <button
                    onClick={() => setSelectedMine(null)}
                    className="p-2 hover:bg-dark-elevated rounded-lg transition"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
                <span
                  className={`inline-block px-4 py-2 rounded-full text-sm font-semibold ${
                    selectedMine.type === 'legal'
                      ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                      : 'bg-red-500/20 text-red-400 border border-red-500/30'
                  }`}
                >
                  {selectedMine.type === 'legal' ? '✓ Authorized Mining Site' : '⚠ Unauthorized Activity Detected'}
                </span>
              </div>

              {/* Panel Content */}
              <div className="p-6 space-y-6">
                {/* Key Metrics */}
                <div>
                  <h3 className="font-semibold text-lg mb-4">Excavation Metrics</h3>
                  <div className="space-y-3">
                  <div className="flex justify-between items-center p-4 bg-dark-elevated rounded-xl">
                    <div>
                      <span className="text-dark-muted text-sm">Total Area</span>
                      <p className="text-xs text-dark-muted/60 mt-1">Surface excavation area</p>
                    </div>
                    <span className="font-bold text-xl">
                      {(selectedMine.area_hectares || selectedMine.area || 0).toFixed(2)} ha
                    </span>
                  </div>
                  <div className="flex justify-between items-center p-4 bg-dark-elevated rounded-xl">
                    <div>
                      <span className="text-dark-muted text-sm">Maximum Depth</span>
                      <p className="text-xs text-dark-muted/60 mt-1">Deepest excavation point</p>
                    </div>
                    <span className="font-bold text-xl">
                      {(selectedMine.depth_m || selectedMine.depth || 0).toFixed(1)} m
                    </span>
                  </div>
                  <div className="flex justify-between items-center p-4 bg-dark-elevated rounded-xl">
                    <div>
                      <span className="text-dark-muted text-sm">Estimated Volume</span>
                      <p className="text-xs text-dark-muted/60 mt-1">Total material excavated</p>
                    </div>
                    <span className="font-bold text-xl">
                      {((selectedMine.volume_m3 || selectedMine.volume || 0) / 1000000).toFixed(2)}M m³
                    </span>
                  </div>
                  </div>
                </div>

                {/* Additional Details */}
                <div>
                  <h3 className="font-semibold text-lg mb-4">Site Information</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between text-sm">
                      <span className="text-dark-muted">Perimeter</span>
                      <span className="font-medium">
                        {(selectedMine.perimeter_km || selectedMine.perimeter_m / 1000 || selectedMine.perimeter || 0).toFixed(2)} km
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-dark-muted">Average Elevation</span>
                      <span className="font-medium">
                        {(selectedMine.avg_elevation_m || selectedMine.avgElevation || 0).toFixed(0)} m ASL
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-dark-muted">Elevation Range</span>
                      <span className="font-medium">
                        {(selectedMine.min_elevation_m || 0).toFixed(0)} - {(selectedMine.max_elevation_m || 0).toFixed(0)} m
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-dark-muted">Primary Material</span>
                      <span className="font-medium">{selectedMine.material || 'Coal'}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-dark-muted">Site Status</span>
                      <span className="font-medium">{selectedMine.detected_material || 'Active Excavation'}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-dark-muted">Operator</span>
                      <span className="font-medium">{selectedMine.operator || 'Unknown'}</span>
                    </div>
                    {selectedMine.type === 'legal' && (
                      <>
                        <div className="flex justify-between text-sm">
                          <span className="text-dark-muted">Last Inspection</span>
                          <span className="font-medium">{selectedMine.last_inspection || selectedMine.lastInspection || 'N/A'}</span>
                        </div>
                        <div className="flex justify-between text-sm items-center">
                          <span className="text-dark-muted">Compliance Status</span>
                          <div className="flex items-center space-x-2">
                            <span className="font-medium text-green-400">{selectedMine.compliance_status || 'Compliant'}</span>
                            <CheckCircle className="w-4 h-4 text-green-400" />
                          </div>
                        </div>
                      </>
                    )}
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="space-y-2">
                  <button className="btn-primary w-full">
                    <Activity className="w-4 h-4 inline mr-2" />
                    View Detailed Analysis Report
                  </button>
                  {selectedMine.type === 'illegal' && (
                    <button className="w-full px-4 py-2 rounded-lg bg-red-500/20 text-red-400 border border-red-500/30 hover:bg-red-500/30 transition">
                      <AlertTriangle className="w-4 h-4 inline mr-2" />
                      Report Unauthorized Activity
                    </button>
                  )}
                  {selectedMine.type === 'legal' && (
                    <button className="w-full px-4 py-2 rounded-lg bg-blue-500/20 text-blue-400 border border-blue-500/30 hover:bg-blue-500/30 transition">
                      <CheckCircle className="w-4 h-4 inline mr-2" />
                      View Compliance Records
                    </button>
                  )}
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  )
}

export default MapView
