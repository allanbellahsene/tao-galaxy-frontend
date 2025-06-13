const express = require('express');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');
const { promisify } = require('util');

const execAsync = promisify(exec);
const readFileAsync = promisify(fs.readFile);
const router = express.Router();

// Get list of available reports
router.get('/list', async (req, res) => {
  try {
    const reportsDir = path.join(__dirname, '../../reports/subnet-reports/output/reports');
    const files = await fs.promises.readdir(reportsDir);
    
    const reports = files
      .filter(file => file.endsWith('.html'))
      .map(file => {
        const subnetId = file.replace('.html', '').replace('SN', '');
        return {
          id: subnetId,
          title: `Subnet ${subnetId} Report`,
          description: `Institutional grade analysis for Subnet ${subnetId}`,
          type: 'Institutional Report',
          date: new Date().toISOString().split('T')[0],
          category: 'Analysis',
          pages: 1,
          premium: true
        };
      });

    res.json(reports);
  } catch (error) {
    console.error('Error listing reports:', error);
    res.status(500).json({ error: 'Failed to list reports' });
  }
});

// Get report for a specific subnet
router.get('/subnet/:subnetId', async (req, res) => {
  try {
    const { subnetId } = req.params;
    let reportPath = path.join(__dirname, '../../reports/subnet-reports/output/reports', `SN${subnetId}.html`);
    
    console.log('Looking for report at:', reportPath);
    console.log('File exists:', fs.existsSync(reportPath));
    
    // If the requested report doesn't exist, try SN1 as fallback
    if (!fs.existsSync(reportPath) && subnetId !== '1') {
      reportPath = path.join(__dirname, '../../reports/subnet-reports/output/reports', 'SN1.html');
      console.log('Fallback to SN1 report at:', reportPath);
      console.log('SN1 file exists:', fs.existsSync(reportPath));
    }
    
    if (fs.existsSync(reportPath)) {
      const reportContent = await readFileAsync(reportPath, 'utf-8');
      res.json({ 
        content: reportContent,
        fallback: subnetId !== '1' && !fs.existsSync(path.join(__dirname, '../../reports/subnet-reports/output/reports', `SN${subnetId}.html`))
      });
    } else {
      res.status(404).json({ error: 'Report not found' });
    }
  } catch (error) {
    console.error('Error getting report:', error);
    res.status(500).json({ error: 'Failed to get report' });
  }
});

// Generate a new report for a subnet
router.post('/generate/:subnetId', async (req, res) => {
  try {
    const { subnetId } = req.params;
    const scriptPath = path.join(__dirname, '../../reports/subnet-reports/scripts/generate-report.js');
    
    // Execute the report generation script
    await execAsync(`node ${scriptPath} ${subnetId}`);
    
    res.json({ message: 'Report generation started', subnetId });
  } catch (error) {
    console.error('Error generating report:', error);
    res.status(500).json({ error: 'Failed to generate report' });
  }
});

module.exports = router; 