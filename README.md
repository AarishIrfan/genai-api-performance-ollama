# GenAI API Performance Framework

## Overview
This framework provides comprehensive performance testing and monitoring for GenAI APIs, specifically focused on Ollama implementation.

## Performance Test Results
<img width="591" height="265" alt="image" src="https://github.com/user-attachments/assets/cc48bc23-d524-49dc-a04f-b0451f6f2360" />

Our latest performance test shows:
- **Total Requests:** 25
- **Successful:** 4 
- **Failed:** 21
- **Average Response Time:** 72.934s
- **Requests/Second:** 0.0


## Features
- Real-time performance monitoring
- Load and stress testing capabilities
- Detailed performance reports
- Grafana dashboards for visualization
- Automated testing suite

## Quick Start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   cd backend && npm install
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```

3. Run tests:
   ```bash
   python scripts/run_tests.py
   ```

## Project Structure
- `/src` - Core implementation
- `/tests` - Test suites
- `/reports` - Performance reports
- `/jmeter` - JMeter test plans
- `/backend` - Node.js API server

## Configuration
See `config/` directory for configuration options:
- `settings.py` - Python configuration
- `jmeter.properties` - JMeter settings
- `ollama.yaml` - Ollama model configuration

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.
