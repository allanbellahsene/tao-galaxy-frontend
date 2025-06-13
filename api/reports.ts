import express from 'express';
import path from 'path';
import fs from 'fs';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);
const readFileAsync = promisify(fs.readFile);
const router = express.Router();

// Get list of available reports
router.get('/list', async (req, res) => {
  try {
    const reportsDir = path.join(process.cwd(), 'tao_galaxy_reports/subnet-reports/output/reports');
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
    const reportPath = path.join(process.cwd(), 'tao_galaxy_reports/subnet-reports/output/reports', `SN${subnetId}.html`);
    
    if (fs.existsSync(reportPath)) {
      const reportContent = await readFileAsync(reportPath, 'utf-8');
      res.json({ content: reportContent });
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
    const scriptPath = path.join(process.cwd(), 'tao_galaxy_reports/subnet-reports/scripts/generate-report.js');
    
    // Execute the report generation script
    await execAsync(`node ${scriptPath} ${subnetId}`);
    
    res.json({ message: 'Report generation started', subnetId });
  } catch (error) {
    console.error('Error generating report:', error);
    res.status(500).json({ error: 'Failed to generate report' });
  }
});

export default router; 