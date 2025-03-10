# Deployment Guide

This guide provides step-by-step instructions for deploying the Disney Data Portfolio project.

## Prerequisites

1. **Python Environment**
   - Python 3.8 or higher
   - pip package manager
   - virtualenv or venv module

2. **Required Software**
   - Git
   - Visual Studio Code (recommended)
   - Node.js and npm (for website)

3. **API Keys**
   - TMDB API key
   - Theme Park API key
   - Weather API key

## Initial Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/[your-username]/disney-data-portfolio.git
   cd disney-data-portfolio
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Unix/MacOS:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r scripts/data_collection/requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   TMDB_API_KEY=your_tmdb_api_key
   THEME_PARK_API_KEY=your_theme_park_api_key
   WEATHER_API_KEY=your_weather_api_key
   ```

## Data Collection Setup

1. **Initialize Data Directories**
   ```bash
   python scripts/deployment/init_directories.py
   ```

2. **Test Data Collection**
   ```bash
   python scripts/tests/test_system.py
   ```

3. **Start Data Collection Service**
   ```bash
   python scripts/data_collection/schedule_collection.py
   ```

## Analytics Pipeline Setup

1. **Process Initial Data**
   ```bash
   python scripts/data_processing/data_processor.py
   ```

2. **Run Analytics**
   ```bash
   python scripts/analytics/analyzer.py
   ```

3. **Generate Reports**
   ```bash
   python scripts/reporting/report_generator.py
   ```

## Website Deployment

1. **Install Website Dependencies**
   ```bash
   cd website
   npm install
   ```

2. **Build Website**
   ```bash
   npm run build
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```

## Monitoring and Maintenance

1. **Check Logs**
   - Data collection logs: `data_collection.log`
   - Analytics logs: `analytics.log`
   - Report generation logs: `reporting.log`

2. **Monitor Data Quality**
   ```bash
   python scripts/monitoring/data_quality_check.py
   ```

3. **Update Dependencies**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

## Troubleshooting

### Common Issues

1. **API Rate Limiting**
   - Check API quotas
   - Adjust collection schedules
   - Implement retry mechanisms

2. **Data Processing Errors**
   - Verify data formats
   - Check for missing values
   - Review validation rules

3. **Report Generation Issues**
   - Ensure data availability
   - Check file permissions
   - Verify template integrity

### Error Resolution

1. **Missing Data**
   ```bash
   python scripts/maintenance/verify_data.py
   python scripts/maintenance/repair_data.py
   ```

2. **Failed Collections**
   ```bash
   python scripts/maintenance/retry_failed_collections.py
   ```

3. **Database Issues**
   ```bash
   python scripts/maintenance/verify_database.py
   python scripts/maintenance/optimize_database.py
   ```

## Backup and Recovery

1. **Backup Data**
   ```bash
   python scripts/maintenance/backup_data.py
   ```

2. **Restore Data**
   ```bash
   python scripts/maintenance/restore_data.py --backup-file [filename]
   ```

## Security Considerations

1. **API Keys**
   - Store securely in environment variables
   - Rotate regularly
   - Monitor usage

2. **Data Protection**
   - Implement access controls
   - Encrypt sensitive data
   - Regular security audits

3. **Access Management**
   - Use role-based access
   - Monitor user activities
   - Regular permission reviews

## Performance Optimization

1. **Data Collection**
   - Optimize collection intervals
   - Implement caching
   - Use incremental updates

2. **Analytics**
   - Optimize queries
   - Implement parallel processing
   - Use data partitioning

3. **Website**
   - Enable caching
   - Optimize assets
   - Implement CDN

## Updating the System

1. **Code Updates**
   ```bash
   git pull origin main
   pip install -r requirements.txt
   ```

2. **Database Schema Updates**
   ```bash
   python scripts/maintenance/update_schema.py
   ```

3. **Configuration Updates**
   ```bash
   python scripts/maintenance/update_config.py
   ```

## Contact and Support

For issues and support:
- GitHub Issues: [repository-url]/issues
- Email: [your-email]
- Documentation: [docs-url] 