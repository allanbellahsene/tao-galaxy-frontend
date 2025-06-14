# TAO Galaxy - Bittensor, Made Easy

A comprehensive platform for exploring, analyzing, and staying updated on the Bittensor ecosystem. TAO Galaxy provides an interactive subnet explorer, institutional-grade AI-powered reports, and real-time news aggregation.

## 🌟 Features

- **🌌 Interactive Subnet Explorer**: Visualize the Bittensor ecosystem with an interactive galaxy map
- **📊 Institutional-Grade Reports**: Professional subnet analysis with market research, TAM calculations, and investment recommendations
- **📰 News Aggregation**: Stay updated with the latest Bittensor and crypto news
- **🔍 Subnet Search & Filtering**: Advanced search and filtering capabilities
- **📱 Responsive Design**: Beautiful, modern UI that works on all devices
- **🤖 AI-Powered Analysis**: Automated research pipeline with competitive analysis and risk assessment

## 🏗️ Project Structure

```
TAO_GALAXY/
├── frontend/                 # React + TypeScript frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── GalaxyView/  # Interactive subnet visualization
│   │   │   ├── SubnetReport/# Institutional report viewer
│   │   │   ├── ReportsView/ # Reports dashboard
│   │   │   ├── NewsView/    # News aggregation
│   │   │   └── Layout/      # Shared layout components
│   │   ├── api/            # API client functions
│   │   ├── context/         # React context providers
│   │   ├── types/           # TypeScript type definitions
│   │   └── utils/           # Utility functions
│   ├── public/              # Static assets and data files
│   └── package.json         # Frontend dependencies
├── backend/                 # Python data processing & Node.js API
│   ├── server/             # Node.js Express API server
│   │   ├── reportApi.js    # Main API server
│   │   ├── reports.js      # Reports router
│   │   └── package.json    # API dependencies
│   ├── data/               # Data processing scripts
│   ├── agents/             # AI research agents
│   ├── reports/            # Generated analysis reports
│   ├── *.py               # Core Python scripts
│   └── requirements.txt     # Python dependencies
├── reports/                # Institutional report generation system
│   └── subnet-reports/     # HTML report templates & output
│       ├── output/         # Generated HTML reports
│       ├── templates/      # Handlebars templates
│       ├── scripts/        # Report generation scripts
│       └── data/           # Research data
├── context_data/           # Global context and documentation
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- **Node.js 18+** and npm
- **Python 3.8+** (for backend data processing)

### 1. Clone and Setup

```bash
git clone https://github.com/allanbellahsene/tao-galaxy-frontend.git
cd tao-galaxy-frontend
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173` (or next available port)

### 3. Backend API Setup (Required for Reports)

```bash
cd backend/server
npm install
npm start
```

The API server will run on `http://localhost:3001`

### 4. Python Environment (Optional - for data processing)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🎯 Available Features

### 🌌 Galaxy View (`/app`)
Interactive 3D visualization of the Bittensor subnet ecosystem:
- **Real-time Data**: Live subnet metrics and performance indicators
- **Category Organization**: Subnets grouped by functionality (AI, Storage, Compute, etc.)
- **Interactive Navigation**: Zoom, pan, and click for detailed information
- **Search & Filter**: Find specific subnets or filter by categories
- **Performance Metrics**: Emission rates, validator counts, and market data

### 📊 Institutional Reports (`/app/reports` & `/app/subnet/:id`)
Professional-grade subnet analysis reports featuring:
- **Executive Summary**: Investment ratings and recommendations
- **Market Analysis**: TAM calculations, competitive landscape, and positioning
- **Team Assessment**: Founder backgrounds and governance structure
- **Financial Analysis**: Revenue potential and sustainability metrics
- **Risk Assessment**: Technical, market, and regulatory risk evaluation
- **Comparative Metrics**: Development momentum and innovation scores

### 📰 News Feed (`/app/news`)
Curated news aggregation with:
- Latest Bittensor ecosystem updates
- Crypto market news and analysis
- Subnet-specific announcements
- Daily market recaps and insights

## 🔧 API Endpoints

The backend API provides the following endpoints:

### Reports API
- `GET /api/reports/list` - List all available subnet reports
- `GET /api/reports/subnet/:id` - Get specific subnet report (HTML)
- `POST /api/reports/generate/:id` - Generate new report for subnet
- `GET /api/health` - API health check

### Data API
- `GET /api/subnet-report/:id` - Get text-based research data
- `GET /api/reports` - List available research reports

## 🛠️ Development

### Frontend Development
```bash
cd frontend
npm run dev     # Start development server
npm run build   # Build for production
npm run lint    # Run ESLint
npm run preview # Preview production build
```

### Backend Development
```bash
cd backend/server
npm run dev     # Start with nodemon (auto-reload)
npm start       # Start production server
```

### Data Processing
```bash
cd backend
python daily_update.py           # Update subnet data
python sync_to_frontend.py       # Sync processed data to frontend
python get_subnet_stats.py       # Fetch latest subnet statistics
```

## 🏗️ Architecture

### Frontend Technologies
- **React 18** with TypeScript for type safety
- **Vite** for fast development and optimized builds
- **Tailwind CSS** for responsive styling
- **D3.js** for interactive data visualizations
- **React Router** for client-side navigation
- **Framer Motion** for smooth animations
- **Lucide React** for consistent iconography

### Backend Technologies
- **Node.js + Express** for API server
- **Python** for data processing and AI analysis
- **Handlebars** for HTML report templating
- **CORS** for cross-origin requests

### Data Flow
1. **Data Collection**: Python scripts gather subnet data from multiple sources
2. **Processing**: Data is cleaned, analyzed, and scored using AI agents
3. **Report Generation**: HTML reports created using Handlebars templates
4. **API Serving**: Express server provides data to frontend
5. **Visualization**: React components render interactive displays

## 🌐 Deployment

### Netlify Deployment (Frontend)
- **Build Command**: `cd frontend && npm install && npm run build`
- **Publish Directory**: `frontend/dist`
- **Node Version**: 18+

### API Server Deployment
The backend API can be deployed to any Node.js hosting service:
- Heroku, Railway, Render, or similar
- Ensure environment variables are configured
- Update frontend API URLs for production

## 📊 Data Sources

- **TaoStats API**: Real-time subnet metrics and validator data
- **GitHub**: Repository activity and development metrics
- **Official Websites**: Project information and documentation
- **News APIs**: Crypto and Bittensor news feeds
- **Market Data**: Token prices and trading volumes

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow TypeScript best practices
- Use Tailwind CSS for styling
- Write meaningful commit messages
- Test your changes thoroughly
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Bittensor Community** for building the decentralized AI ecosystem
- **TaoStats** for providing reliable API access and data
- **Subnet Teams** for their innovation in decentralized AI
- **Open Source Contributors** who make this project possible

---

**Built with ❤️ for the Bittensor community**

For more detailed information about specific features, see:
- [Subnet Reports Documentation](README_SubnetReport.md)
- [API Documentation](backend/README.md)
