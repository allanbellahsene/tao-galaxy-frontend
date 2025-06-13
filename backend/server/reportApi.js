const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3001;

// Enable CORS for frontend requests
app.use(cors());
app.use(express.json());

// Import the /api/reports router (ESM interop)
const reportsRouter = require('./reports');
app.use('/api/reports', reportsRouter);

// Serve subnet report files
app.get('/api/subnet-report/:subnetId', async (req, res) => {
  try {
    const { subnetId } = req.params;
    const reportPath = path.join(__dirname, '..', 'results', 'research', `SN${subnetId}_report.txt`);
    
    // Check if file exists
    try {
      await fs.access(reportPath);
    } catch (error) {
      console.log(`Report file not found: ${reportPath}`);
      return res.status(404).json({ 
        error: `Report not found for subnet ${subnetId}`,
        path: reportPath 
      });
    }
    
    // Read and return the file content
    const reportContent = await fs.readFile(reportPath, 'utf8');
    res.set('Content-Type', 'text/plain');
    res.send(reportContent);
    
  } catch (error) {
    console.error('Error serving report:', error);
    res.status(500).json({ 
      error: 'Internal server error',
      message: error.message 
    });
  }
});

// List available reports
app.get('/api/reports', async (req, res) => {
  try {
    const reportsDir = path.join(__dirname, '..', 'results', 'research');
    const files = await fs.readdir(reportsDir);
    
    const reportFiles = files
      .filter(file => file.endsWith('_report.txt'))
      .map(file => {
        const match = file.match(/SN(\d+)_report\.txt/);
        return match ? {
          subnetId: match[1],
          filename: file,
          path: `/api/subnet-report/${match[1]}`
        } : null;
      })
      .filter(Boolean);
    
    res.json({ reports: reportFiles });
  } catch (error) {
    console.error('Error listing reports:', error);
    res.status(500).json({ 
      error: 'Failed to list reports',
      message: error.message 
    });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    timestamp: new Date().toISOString(),
    service: 'Subnet Report API'
  });
});

app.listen(PORT, () => {
  console.log(`Report API server running on port ${PORT}`);
  console.log(`Available endpoints:`);
  console.log(`  GET /api/health - Health check`);
  console.log(`  GET /api/reports - List available reports`);
  console.log(`  GET /api/subnet-report/:subnetId - Get specific subnet report`);
});

module.exports = app; 