# Scalable Subnet Report System

## Overview

This system provides a scalable solution for generating institutional reports from subnet research data. It's designed to work with text-based report files (like `SN64_report.txt`) and can easily be extended for multiple subnets.

## Architecture

### Frontend Components
- **SubnetReport/index.tsx**: Main React component that renders the report
- **utils/reportParser.ts**: Utility for parsing report text data  
- **api/subnetReport.ts**: API service layer for data loading

### Backend API  
- **server/reportApi.js**: Express server serving report files
- **server/package.json**: Backend dependencies

## Key Features

### ✅ **Scalable Design**
- Accepts `subnetId` prop to render any subnet report
- Dynamic data loading from backend API
- Consistent report structure across all subnets

### ✅ **Data-Driven**
- Parses data from `backend/results/research/SN{ID}_report.txt` files
- Intelligent text parsing with fallback handling
- No hard-coded subnet-specific data

### ✅ **Error Handling**
- Loading states with progress indicators
- Graceful error handling with user-friendly messages
- Fallback data for SN64 if API fails

### ✅ **Professional UI**
- Modern dark theme with responsive design  
- Collapsible sections for better UX
- Export functionality and navigation

## Usage

### Basic Implementation
```tsx
import SubnetReport from './components/SubnetReport';

// Render SN64 report (default)
<SubnetReport />

// Render any subnet report
<SubnetReport subnetId="1" onBack={() => navigate('/subnets')} />
```

### Props Interface
```tsx
interface SubnetReportProps {
  subnetId?: string;     // Default: '64'
  onBack?: () => void;   // Navigation callback
}
```

## Setup Instructions

### 1. Backend Setup
```bash
cd backend/server
npm install
npm start
```

The API server will run on port 3001 with endpoints:
- `GET /api/subnet-report/:subnetId` - Get specific report
- `GET /api/reports` - List available reports  
- `GET /api/health` - Health check

### 2. Frontend Setup
The frontend automatically connects to the backend API. Set environment variable if needed:
```bash
export REACT_APP_API_URL=http://localhost:3001
```

### 3. Data Structure
Place report files in: `backend/results/research/SN{ID}_report.txt`

Example files:
- `SN64_report.txt` (Chutes AI)
- `SN1_report.txt` (Apex)  
- `SN8_report.txt` (Future subnet)

## Data Parsing

The system intelligently parses structured text reports:

### Supported Sections
- **Basic Info**: Name, ID, mission statement
- **Team**: Founding team, doxxed status, organizations
- **Problem**: Market analysis, competitors, TAM
- **Revenue**: Streams, monetization, development phase
- **Marketing**: Channels, frequency, community engagement
- **Development**: Open source status, repositories, practices

### Text Patterns
The parser looks for specific patterns like:
- `### What is [SubnetName]` for mission statements
- `**Team:**` for team information  
- `**Revenue Streams:**` for financial data
- Markdown headers and bold formatting

## Extending for New Subnets

### 1. Add Report File
Create `backend/results/research/SN{NEW_ID}_report.txt` following the same structure as SN64.

### 2. Use Component
```tsx
<SubnetReport subnetId="NEW_ID" />
```

### 3. Customize Parsing (if needed)
Update `parseReportFromText` function in `api/subnetReport.ts` for subnet-specific parsing logic.

## Error Recovery

### Fallback Mechanisms
- API failures → Fallback to hardcoded SN64 data
- Missing sections → "Information not found" placeholders  
- Parse errors → Graceful degradation with user notification

### Development Mode
- Console logging for debugging parse issues
- Health check endpoint for API monitoring
- Detailed error messages in development

## Future Enhancements

### Planned Features
- PDF export functionality
- Real-time data updates
- Advanced filtering/search
- Multiple report formats
- Caching layer for performance

### Scalability Considerations
- Database integration for metadata
- CDN for static report files
- Rate limiting and caching
- Multi-language support

## Technical Details

### Dependencies
**Frontend:**
- React 18+ with TypeScript
- Lucide React icons
- Tailwind CSS for styling

**Backend:**
- Express.js server
- CORS middleware  
- File system API

### File Structure
```
frontend/src/
├── components/SubnetReport/
│   └── index.tsx              # Main component
├── utils/
│   └── reportParser.ts        # Data parsing utilities
└── api/
    └── subnetReport.ts        # API service layer

backend/
├── server/
│   ├── reportApi.js          # Express API server  
│   └── package.json          # Dependencies
└── results/research/
    ├── SN64_report.txt       # Chutes report data
    ├── SN1_report.txt        # Apex report data
    └── SN8_report.txt        # Additional subnet data
```

## Contributing

When adding new subnets:
1. Follow the existing report text structure
2. Test with the `SubnetReport` component
3. Update parsing logic if new data patterns emerge
4. Maintain consistent section headers and formatting

This system is designed to grow with your subnet ecosystem while maintaining consistency and reliability across all reports. 