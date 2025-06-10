# TAO Galaxy Backend - Enhanced Subnet Data Retrieval System

This comprehensive backend system automatically retrieves, enriches, and merges subnet data from multiple TaoStats API endpoints to provide detailed information for the TAO Galaxy frontend.

## 🆕 Latest Features

- **📊 Market Data Integration**: Real-time market cap, price, and trading volume data
- **📈 Percentage-based Emissions**: Emissions shown as percentage of total network emission
- **📅 Daily Historical Data**: Automatic daily snapshots with date-based filenames
- **🔗 Multi-source Data Merging**: Combines identity, statistics, and market data seamlessly
- **📋 Comprehensive Data Schema**: 16 columns of enriched subnet information

## Features

- **Subnet Identity Data**: Names, descriptions, URLs, GitHub repos, Discord channels
- **Subnet Statistics**: Latest emission data (as percentages) and active status
- **Market Data**: Market cap, price, price changes, trading volume, and rankings
- **Data Merging**: Combines all datasets into a comprehensive view
- **Multiple Output Formats**: Saves data as both CSV and JSON
- **Daily Historical Backups**: Date-based files for data continuity
- **Error Handling**: Robust error handling and logging
- **Data Validation**: Ensures data quality and handles missing fields

## Data Schema

The enhanced merged dataset includes the following columns:

| Column | Description | Source |
|--------|-------------|---------|
| Timestamp | When the data was retrieved | System |
| Subnet ID | Unique subnet identifier (netuid) | Identity API |
| Subnet Name | Human-readable subnet name | Identity API |
| Description | Subnet description | Identity API |
| Emission | Current emission as % of total | Statistics API |
| Active | Whether the subnet is active | Statistics API |
| Website | Subnet website URL | Identity API |
| Github | GitHub repository URL | Identity API |
| Discord | Discord contact information | Identity API |
| Rank | Market ranking | Market API |
| Market Cap | Market capitalization in USD | Market API |
| Price | Current price per token | Market API |
| Price Change 1 Day | 24-hour price change % | Market API |
| Price Change 1 Week | 7-day price change % | Market API |
| Price Change 1 Month | 30-day price change % | Market API |
| TAO Volume 24hr | 24-hour trading volume in TAO | Market API |

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the backend directory:

```env
TAOSTATS_API_KEY=your_taostats_api_key_here
```

### 3. API Key Setup

Get your TaoStats API key from [TaoStats.io](https://taostats.io) and add it to your `.env` file.

## Usage

### Quick Start - Enhanced Data Pipeline

Run the complete enhanced data update process:

```bash
python update_subnet_data.py
```

This will:
1. Fetch subnet identity data from TaoStats API (121+ subnets)
2. Fetch latest subnet statistics with percentage-based emissions
3. Fetch market data including prices, volumes, and rankings
4. Merge all datasets into comprehensive view
5. Save current results as CSV and JSON files
6. Create daily historical backup files

### Individual Scripts

You can also run individual components:

```bash
# Get subnet identities only
python get_subnets.py

# Get subnet statistics only  
python get_subnet_stats.py

# Get market data only
python get_market_data.py

# Merge existing data
python merge_subnet_data.py
```

### Daily Automated Updates

For production environments, use the daily scheduler:

```bash
python daily_update.py
```

## Output Files

### Current Data Files
All current files are saved in the `results/` directory:

- `merged_subnet_data.csv` - Complete merged dataset in CSV format
- `merged_subnet_data.json` - Complete merged dataset in JSON format
- `subnet_identities.csv` - Raw subnet identity data
- `subnet_stats.csv` - Raw subnet statistics data
- `market_data.csv` - Raw market data

### Daily Historical Files
Historical files are saved in `results/daily/` with date-based names:

- `subnet_data_YYYY-MM-DD.csv` - Daily snapshot in CSV format
- `subnet_data_YYYY-MM-DD.json` - Daily snapshot in JSON format

Example:
```
results/daily/
├── subnet_data_2025-06-10.csv
├── subnet_data_2025-06-10.json
├── subnet_data_2025-06-11.csv
└── subnet_data_2025-06-11.json
```

## API Endpoints Used

1. **Subnet Identity**: `https://api.taostats.io/api/subnet/identity/v1`
   - Returns subnet names, descriptions, URLs, GitHub repos, Discord channels

2. **Subnet Statistics**: `https://api.taostats.io/api/subnet/latest/v1`
   - Returns emission data, active status, timestamps

3. **Market Data**: `https://api.taostats.io/api/dtao/pool/latest/v1`
   - Returns market cap, prices, price changes, trading volumes, rankings

## Data Processing

### Emission Percentage Calculation
Emissions are automatically converted from absolute values to percentages:
```python
emission_percentage = (subnet_emission / total_network_emission) * 100
```

### Data Merging Process
1. **Base Dataset**: Start with subnet identity data
2. **Statistics Merge**: Join with statistics data on `netuid`
3. **Market Data Merge**: Join with market data on `netuid`
4. **Data Cleaning**: Handle missing values and normalize data types

## Scheduling

### Cron (Linux/Mac)
```bash
# Run daily at 2 AM
0 2 * * * cd /path/to/backend && python daily_update.py

# Run every 6 hours
0 */6 * * * cd /path/to/backend && python daily_update.py
```

### Windows Task Scheduler
Create a task to run `daily_update.py` at your desired interval.

## Data Quality & Validation

The system ensures data quality by:
- Converting data types appropriately (netuid to int, emission to float, etc.)
- Calculating percentage-based emissions for better comparison
- Handling null/missing values with sensible defaults
- Validating API response structure across multiple endpoints
- Providing detailed logging for debugging
- Creating daily backups to prevent data loss

## Logging

All operations are logged with different levels:
- **INFO**: Normal operations, progress updates, data summaries
- **WARNING**: Missing data fields, API inconsistencies
- **ERROR**: Failed operations, API errors, critical issues

Daily logs are saved in the `logs/` directory with date-based filenames.

## Monitoring & Health Checks

The system provides comprehensive monitoring:
- Data completeness reports
- Emission percentage validation
- Market data availability checks
- Historical data consistency
- API response time monitoring

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure `TAOSTATS_API_KEY` is set in your `.env` file
2. **Network Errors**: Check internet connection and API endpoint availability
3. **Permission Errors**: Ensure write permissions for `results/` and `logs/` directories
4. **Missing Dependencies**: Run `pip install -r requirements.txt`
5. **Data Inconsistency**: Check API response format changes

### Debug Mode

For debugging, examine logs in the `logs/` directory or run individual scripts to isolate issues.

## Performance

- **Typical Runtime**: 30-60 seconds for complete data refresh
- **Data Volume**: ~121 subnets with 16 columns each
- **API Calls**: 3 concurrent API calls for optimal performance
- **Storage**: ~30KB CSV, ~67KB JSON per daily snapshot

## License

This project is part of the TAO Galaxy ecosystem. 