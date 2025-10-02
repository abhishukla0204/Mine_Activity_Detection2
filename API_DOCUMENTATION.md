# API Documentation

## Mining Activity Monitoring Tool - REST API

Base URL: `http://localhost:5000/api`

---

## Endpoints

### 1. Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

### 2. Upload Files

**POST** `/upload`

Upload satellite imagery, DEM, and annotations for analysis.

**Form Data:**
- `satellite` (required): Satellite TIF file
- `dem` (required): Digital Elevation Model TIF file
- `annotations` (required): COCO JSON annotations
- `boundary` (optional): Authorized boundary shapefile/GeoJSON

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "uploaded",
  "message": "Files uploaded successfully"
}
```

**Example (curl):**
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "satellite=@satellite.tif" \
  -F "dem=@dem.tif" \
  -F "annotations=@annotations.json"
```

---

### 3. Start Analysis

**POST** `/analyze/<job_id>`

Start the mining detection and analysis process.

**Body (JSON):**
```json
{
  "volume_method": "simpsons",  // Options: simpsons, trapezoidal, monte_carlo
  "reference_elevation": "auto"  // Options: auto, min, max, mean, or numeric value
}
```

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "processing",
  "message": "Analysis started"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/analyze/abc-123 \
  -H "Content-Type: application/json" \
  -d '{"volume_method": "simpsons"}'
```

---

### 4. Get Job Status

**GET** `/status/<job_id>`

Check the status and progress of an analysis job.

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "processing",  // uploaded, processing, completed, failed
  "progress": 65,           // 0-100
  "current_step": "Depth & Volume Calculation",
  "created_at": "2024-11-15T10:30:00"
}
```

**Example:**
```bash
curl http://localhost:5000/api/status/abc-123
```

---

### 5. Get Results

**GET** `/results/<job_id>`

Retrieve analysis results after completion.

**Response:**
```json
{
  "summary": {
    "total_sites": 11,
    "total_area": 152.4,
    "total_volume": 4250000,
    "legal_sites": 7,
    "illegal_sites": 4
  },
  "sites": [
    {
      "id": 1,
      "geometry": {...},
      "area": 15.2,
      "depth": 28,
      "volume": 425000,
      "classification": "legal"
    }
  ],
  "files": {
    "map": "path/to/map.html",
    "report": "path/to/report.html"
  }
}
```

---

### 6. Download Files

**GET** `/download/<job_id>/<file_type>`

Download generated files (map, report, etc.).

**File Types:**
- `map`: Interactive HTML map
- `report`: HTML analysis report
- `geojson`: Mining areas as GeoJSON
- `pdf`: PDF report (if generated)

**Example:**
```bash
curl -O http://localhost:5000/api/download/abc-123/report
```

---

### 7. List All Jobs

**GET** `/jobs`

List all analysis jobs.

**Response:**
```json
[
  {
    "job_id": "uuid-1",
    "status": "completed",
    "progress": 100,
    "created_at": "2024-11-15T10:30:00"
  },
  {
    "job_id": "uuid-2",
    "status": "processing",
    "progress": 45,
    "created_at": "2024-11-15T11:00:00"
  }
]
```

---

### 8. Get Statistics

**GET** `/stats`

Get aggregated statistics from all analyses.

**Response:**
```json
{
  "total_analyses": 5,
  "total_sites": 11,
  "total_area": 152.4,
  "legal_area": 98.6,
  "illegal_area": 53.8,
  "total_violations": 4,
  "total_volume": 4250000,
  "average_depth": 26.4
}
```

---

## Analysis Pipeline

The analysis pipeline consists of 6 steps:

1. **Loading Data** (0-20%)
   - Load satellite imagery, DEM, and annotations
   - Validate coordinate systems

2. **Detecting Mining Areas** (20-40%)
   - Extract polygons from COCO annotations
   - Calculate basic metrics (area, perimeter)

3. **Boundary Analysis** (40-60%)
   - Compare with authorized boundaries
   - Classify as legal/illegal

4. **Depth & Volume Calculation** (60-80%)
   - Estimate reference elevation
   - Calculate depth maps
   - Compute volumes using Simpson's Rule

5. **Generating Visualizations** (80-90%)
   - Create interactive 2D maps
   - Generate 3D terrain models
   - Create charts and heatmaps

6. **Generating Report** (90-100%)
   - Compile statistics
   - Generate HTML report
   - Export GeoJSON data

---

## Error Responses

All endpoints return standard error responses:

```json
{
  "error": "Error message description"
}
```

**HTTP Status Codes:**
- `200`: Success
- `400`: Bad Request (missing parameters, invalid data)
- `404`: Not Found (job not found)
- `500`: Internal Server Error

---

## Usage Example (Python)

```python
import requests
import time

API_BASE = "http://localhost:5000/api"

# 1. Upload files
files = {
    'satellite': open('satellite.tif', 'rb'),
    'dem': open('dem.tif', 'rb'),
    'annotations': open('annotations.json', 'rb')
}
response = requests.post(f"{API_BASE}/upload", files=files)
job_id = response.json()['job_id']
print(f"Job created: {job_id}")

# 2. Start analysis
config = {'volume_method': 'simpsons'}
response = requests.post(f"{API_BASE}/analyze/{job_id}", json=config)
print("Analysis started")

# 3. Poll for status
while True:
    response = requests.get(f"{API_BASE}/status/{job_id}")
    status = response.json()
    print(f"Progress: {status['progress']}% - {status['current_step']}")
    
    if status['status'] == 'completed':
        break
    elif status['status'] == 'failed':
        print("Analysis failed")
        exit(1)
    
    time.sleep(5)

# 4. Get results
response = requests.get(f"{API_BASE}/results/{job_id}")
results = response.json()
print(f"Found {results['summary']['total_sites']} mining sites")

# 5. Download report
response = requests.get(f"{API_BASE}/download/{job_id}/report")
with open('report.html', 'wb') as f:
    f.write(response.content)
print("Report downloaded")
```

---

## Usage Example (JavaScript/React)

```javascript
import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

// 1. Upload files
const uploadFiles = async (files) => {
  const formData = new FormData();
  formData.append('satellite', files.satellite);
  formData.append('dem', files.dem);
  formData.append('annotations', files.annotations);
  
  const response = await axios.post(`${API_BASE}/upload`, formData);
  return response.data.job_id;
};

// 2. Start analysis
const startAnalysis = async (jobId, config) => {
  const response = await axios.post(
    `${API_BASE}/analyze/${jobId}`,
    config
  );
  return response.data;
};

// 3. Poll for status
const pollStatus = async (jobId, onProgress) => {
  const interval = setInterval(async () => {
    const response = await axios.get(`${API_BASE}/status/${jobId}`);
    const status = response.data;
    
    onProgress(status);
    
    if (status.status === 'completed' || status.status === 'failed') {
      clearInterval(interval);
    }
  }, 2000);
};

// 4. Get results
const getResults = async (jobId) => {
  const response = await axios.get(`${API_BASE}/results/${jobId}`);
  return response.data;
};

// Usage
const runAnalysis = async () => {
  const jobId = await uploadFiles(selectedFiles);
  await startAnalysis(jobId, { volume_method: 'simpsons' });
  
  await pollStatus(jobId, (status) => {
    console.log(`Progress: ${status.progress}%`);
  });
  
  const results = await getResults(jobId);
  console.log(results);
};
```

---

## WebSocket Support (Future)

For real-time updates, WebSocket support will be added:

```javascript
const ws = new WebSocket('ws://localhost:5000/ws/analysis/' + jobId);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Progress:', data.progress, '%');
};
```

---

## Rate Limiting

Currently no rate limiting is implemented. In production, consider:
- Max 10 uploads per hour per IP
- Max 5 concurrent analysis jobs per user
- Max file size: 100MB per upload

---

## Security Considerations

For production deployment:
1. Add authentication (JWT tokens)
2. Implement HTTPS
3. Validate file contents (not just extensions)
4. Implement virus scanning
5. Add rate limiting
6. Use persistent storage (database)
7. Implement user quotas
