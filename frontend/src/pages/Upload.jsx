import { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion } from 'framer-motion'
import { Upload, File, X, Check, AlertCircle, Play } from 'lucide-react'

const UploadPage = () => {
  const [files, setFiles] = useState({
    satellite: null,
    dem: null,
    annotations: null,
    boundary: null,
  })

  const [uploading, setUploading] = useState(false)
  const [analysisStatus, setAnalysisStatus] = useState(null)

  const createDropzone = (fileType) => {
    return useDropzone({
      onDrop: (acceptedFiles) => {
        if (acceptedFiles.length > 0) {
          setFiles((prev) => ({ ...prev, [fileType]: acceptedFiles[0] }))
        }
      },
      maxFiles: 1,
    })
  }

  const satelliteDropzone = createDropzone('satellite')
  const demDropzone = createDropzone('dem')
  const annotationsDropzone = createDropzone('annotations')
  const boundaryDropzone = createDropzone('boundary')

  const removeFile = (fileType) => {
    setFiles((prev) => ({ ...prev, [fileType]: null }))
  }

  const handleAnalysis = async () => {
    if (!files.satellite || !files.dem || !files.annotations) {
      alert('Please upload at least Satellite Image, DEM, and Annotations')
      return
    }

    setUploading(true)
    setAnalysisStatus('uploading')

    // Simulate upload and analysis
    setTimeout(() => {
      setAnalysisStatus('processing')
      setTimeout(() => {
        setAnalysisStatus('completed')
        setUploading(false)
      }, 3000)
    }, 2000)
  }

  const DropzoneCard = ({ dropzone, fileType, title, description, file, required = false }) => {
    return (
      <div className="card">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="font-bold flex items-center">
              {title}
              {required && <span className="ml-2 text-red-400 text-sm">*</span>}
            </h3>
            <p className="text-sm text-dark-muted">{description}</p>
          </div>
          {file && (
            <button
              onClick={() => removeFile(fileType)}
              className="p-1 hover:bg-red-500/20 rounded transition"
            >
              <X className="w-5 h-5 text-red-400" />
            </button>
          )}
        </div>

        {file ? (
          <div className="p-4 bg-dark-elevated rounded-lg flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Check className="w-5 h-5 text-green-400" />
              <div>
                <p className="font-medium">{file.name}</p>
                <p className="text-sm text-dark-muted">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
          </div>
        ) : (
          <div
            {...dropzone.getRootProps()}
            className="border-2 border-dashed border-dark-border rounded-lg p-8 text-center cursor-pointer hover:border-primary-500 hover:bg-dark-elevated transition"
          >
            <input {...dropzone.getInputProps()} />
            <Upload className="w-12 h-12 mx-auto mb-4 text-dark-muted" />
            <p className="text-dark-muted">
              Drag & drop file here, or click to select
            </p>
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold gradient-text mb-2">
          Upload Data & Run Analysis
        </h1>
        <p className="text-dark-muted">
          Upload satellite imagery, DEM, and annotations to detect mining activities
        </p>
      </div>

      {/* File Upload Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DropzoneCard
          dropzone={satelliteDropzone}
          fileType="satellite"
          title="Satellite Imagery"
          description="Sentinel-2 RGB TIF (10m resolution)"
          file={files.satellite}
          required
        />

        <DropzoneCard
          dropzone={demDropzone}
          fileType="dem"
          title="Digital Elevation Model"
          description="SRTM DEM TIF (30m resolution)"
          file={files.dem}
          required
        />

        <DropzoneCard
          dropzone={annotationsDropzone}
          fileType="annotations"
          title="Mining Annotations"
          description="COCO JSON format from Roboflow"
          file={files.annotations}
          required
        />

        <DropzoneCard
          dropzone={boundaryDropzone}
          fileType="boundary"
          title="Authorized Boundary (Optional)"
          description="Shapefile, KML, or GeoJSON"
          file={files.boundary}
        />
      </div>

      {/* Configuration Options */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card"
      >
        <h3 className="font-bold mb-4">Analysis Configuration</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">
              Volume Calculation Method
            </label>
            <select className="input-field w-full">
              <option value="simpsons">Simpson's Rule</option>
              <option value="trapezoidal">Trapezoidal</option>
              <option value="montecarlo">Monte Carlo</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Reference Elevation
            </label>
            <select className="input-field w-full">
              <option value="mean">Mean</option>
              <option value="median">Median</option>
              <option value="max">Maximum</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Minimum Mining Area
            </label>
            <input
              type="number"
              defaultValue={100}
              className="input-field w-full"
              placeholder="pixels"
            />
          </div>
        </div>
      </motion.div>

      {/* Action Buttons */}
      <div className="flex items-center space-x-4">
        <button
          onClick={handleAnalysis}
          disabled={uploading || !files.satellite || !files.dem || !files.annotations}
          className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {uploading ? (
            <>
              <div className="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full inline-block mr-2" />
              Processing...
            </>
          ) : (
            <>
              <Play className="w-5 h-5 inline mr-2" />
              Start Analysis
            </>
          )}
        </button>

        <button className="btn-secondary">
          Load Example Data
        </button>
      </div>

      {/* Analysis Status */}
      {analysisStatus && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
        >
          <h3 className="font-bold mb-4">Analysis Progress</h3>
          
          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                analysisStatus === 'uploading' ? 'bg-primary-500 animate-pulse' : 'bg-green-500'
              }`}>
                {analysisStatus !== 'uploading' ? <Check className="w-5 h-5" /> : '1'}
              </div>
              <div className="flex-1">
                <p className="font-medium">Uploading Files</p>
                <div className="w-full bg-dark-elevated rounded-full h-2 mt-2">
                  <div className={`h-2 rounded-full bg-primary-500 transition-all duration-500 ${
                    analysisStatus === 'uploading' ? 'w-1/2' : 'w-full'
                  }`} />
                </div>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                analysisStatus === 'processing' ? 'bg-primary-500 animate-pulse' : 
                analysisStatus === 'completed' ? 'bg-green-500' : 'bg-dark-elevated'
              }`}>
                {analysisStatus === 'completed' ? <Check className="w-5 h-5" /> : '2'}
              </div>
              <div className="flex-1">
                <p className="font-medium">Processing & Analysis</p>
                {analysisStatus === 'processing' && (
                  <div className="w-full bg-dark-elevated rounded-full h-2 mt-2">
                    <div className="h-2 rounded-full bg-primary-500 animate-pulse w-3/4" />
                  </div>
                )}
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                analysisStatus === 'completed' ? 'bg-green-500' : 'bg-dark-elevated'
              }`}>
                {analysisStatus === 'completed' ? <Check className="w-5 h-5" /> : '3'}
              </div>
              <p className="font-medium">Generating Reports</p>
            </div>
          </div>

          {analysisStatus === 'completed' && (
            <div className="mt-6 p-4 bg-green-500/10 border border-green-500/30 rounded-lg">
              <div className="flex items-start space-x-3">
                <Check className="w-6 h-6 text-green-400 flex-shrink-0" />
                <div>
                  <h4 className="font-bold text-green-400 mb-2">Analysis Complete!</h4>
                  <p className="text-sm text-dark-muted mb-4">
                    Successfully detected 11 mining sites. View results and generate reports.
                  </p>
                  <div className="flex space-x-3">
                    <button className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition">
                      View Results
                    </button>
                    <button className="px-4 py-2 bg-dark-elevated border border-dark-border rounded-lg hover:bg-dark-surface transition">
                      Download Report
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </motion.div>
      )}

      {/* Info Box */}
      <div className="card bg-blue-500/10 border-blue-500/30">
        <div className="flex items-start space-x-3">
          <AlertCircle className="w-6 h-6 text-blue-400 flex-shrink-0" />
          <div>
            <h4 className="font-bold text-blue-400 mb-2">Data Requirements</h4>
            <ul className="text-sm text-dark-muted space-y-1">
              <li>• Satellite Image: TIF format, 10m resolution recommended</li>
              <li>• DEM: TIF format, SRTM 30m or better</li>
              <li>• Annotations: COCO JSON format with mining area polygons</li>
              <li>• Boundary (optional): Shapefile, KML, or GeoJSON for authorized areas</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default UploadPage
