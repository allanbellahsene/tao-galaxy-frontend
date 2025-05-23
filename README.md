# TAO Galaxy - Bittensor Subnet Explorer

A comprehensive dashboard for exploring, analyzing, and staying updated on the Bittensor ecosystem. TAO Galaxy provides an interactive subnet explorer, AI-powered reports, and real-time news aggregation.

## 🌟 Features

- **🌌 Interactive Subnet Explorer**: Visualize the Bittensor ecosystem with an interactive galaxy map
- **📊 AI-Powered Reports**: Comprehensive subnet analysis with automated research pipeline
- **📰 News Aggregation**: Stay updated with the latest Bittensor and crypto news
- **🔍 Subnet Search & Filtering**: Advanced search and filtering capabilities
- **📱 Responsive Design**: Beautiful, modern UI that works on all devices

## 🏗️ Project Structure

```
TAO_GALAXY/
├── frontend/                 # React + TypeScript frontend application
│   ├── src/                 # Source code
│   │   ├── components/      # React components
│   │   ├── context/         # React context providers
│   │   ├── types/           # TypeScript type definitions
│   │   └── utils/           # Utility functions
│   ├── public/              # Static assets and data files
│   ├── package.json         # Frontend dependencies
│   └── dist/                # Build output (generated)
├── backend/                 # Python backend for data processing
│   ├── automated_pipeline.py # Main data pipeline
│   ├── research_agent.py    # AI research agent
│   ├── scoring_agent.py     # AI scoring system
│   └── requirements.txt     # Python dependencies
├── data/                    # Processed subnet data
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+ (for backend processing)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/allanbellahsene/tao-galaxy-frontend.git
   cd tao-galaxy-frontend
   ```

2. **Install frontend dependencies:**
   ```bash
   cd frontend
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5173` (or the port shown in your terminal)

### Backend Setup (Optional)

The frontend works with pre-processed data, but you can run the backend pipeline to update subnet information:

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

3. **Run the data pipeline:**
   ```bash
   python automated_pipeline.py
   ```

## 🌐 Production Deployment

This project is configured for deployment on Netlify with the following settings:

- **Build Command**: `cd frontend && npm install && npm run build`
- **Publish Directory**: `frontend/dist`
- **Node Version**: 18+

### Deploy to Netlify

1. Connect your GitHub repository to Netlify
2. Set the build settings as shown above
3. Deploy!

The frontend is completely self-contained in the `frontend/` directory, making deployment straightforward.

## 🎯 Available Pages

### 🌌 Subnet Explorer (`/app`)
Interactive galaxy visualization of all Bittensor subnets with:
- Real-time market data
- Category-based organization
- Zoom and pan functionality
- Detailed subnet information

### 📊 Reports (`/app/reports`)
Comprehensive subnet analysis featuring:
- AI-generated subnet scores
- Market performance metrics
- Technical analysis
- Investment recommendations

### 📰 News (`/app/news`)
Curated news feed with:
- Latest Bittensor updates
- Crypto market news
- Subnet-specific announcements
- Daily market recaps

## 🔧 Development

### Frontend Technologies

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **D3.js** for data visualization
- **React Router** for navigation
- **Framer Motion** for animations

### Code Organization

- `components/GalaxyView/` - Main subnet explorer
- `components/ReportsView/` - Analysis and reports
- `components/NewsView/` - News aggregation
- `components/Layout/` - Shared layout components

### Data Flow

1. Subnet data is processed by the backend pipeline
2. Frontend loads data from `public/subnets_frontend_ready.json`
3. D3.js renders the interactive galaxy visualization
4. React manages state and user interactions

## 📊 Data Sources

- **TaoStats API** - Real-time subnet metrics
- **GitHub** - Subnet source code and activity
- **Official Websites** - Project information and updates
- **News APIs** - Crypto and Bittensor news feeds

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Bittensor community for the innovative subnet ecosystem
- TaoStats for providing reliable API access
- All subnet teams building the future of decentralized AI

---

**Built with ❤️ for the Bittensor community** 