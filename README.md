# Member 360 Agentic AI

A comprehensive member management system powered by Azure services and AI capabilities, featuring advanced agentic AI interactions.

## Features

### Core Features
- Member profile management with interactive dashboard
- Document intelligence for member documents
- AI-powered member insights and recommendations
- Streamlit-based modern user interface
- Azure Cosmos DB for data storage
- AutoGen for agentic AI capabilities
- Semantic Kernel for AI orchestration

### Agentic AI Features
- **Intelligent Member Interactions**
  - AI-powered conversation agents for member support
  - Automated follow-up and engagement tracking
  - Smart interaction recommendations based on member history
  - Natural language processing for member communications

- **Document Intelligence**
  - Automated document processing and classification
  - Intelligent document verification and validation
  - AI-powered document insights extraction
  - Smart document status tracking and alerts

- **Member Insights & Analytics**
  - AI-driven member behavior analysis
  - Predictive engagement scoring
  - Automated member segmentation
  - Smart recommendation engine for member actions

- **Automated Workflows**
  - AI-powered task automation
  - Smart workflow orchestration
  - Automated decision support
  - Intelligent process optimization

## Prerequisites

- Python 3.9+
- Azure subscription
- Azure Cosmos DB account
- Azure OpenAI service
- Azure Document Intelligence service

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Azure credentials:
   ```
   AZURE_COSMOS_ENDPOINT=your_cosmos_endpoint
   AZURE_COSMOS_KEY=your_cosmos_key
   AZURE_OPENAI_API_KEY=your_openai_key
   AZURE_OPENAI_ENDPOINT=your_openai_endpoint
   AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=your_document_intelligence_endpoint
   AZURE_DOCUMENT_INTELLIGENCE_KEY=your_document_intelligence_key
   ```

## Running the Application

```bash
streamlit run app.py
```

## Project Structure

- `app.py`: Main Streamlit application with interactive UI
- `database/`: Cosmos DB setup and operations
- `agents/`: AutoGen agent configurations
  - `member_agent.py`: Member interaction and support agent
  - `document_agent.py`: Document processing and analysis agent
  - `insights_agent.py`: Member insights and analytics agent
- `semantic_kernel/`: Semantic Kernel configurations
  - `skills/`: AI skills and capabilities
  - `planner/`: Task planning and orchestration
- `utils/`: Utility functions
- `data/`: Sample data and data generation scripts

## Agentic AI Architecture

The system uses a multi-agent architecture powered by AutoGen and Semantic Kernel:

1. **Member Agent**
   - Handles member interactions and support
   - Provides personalized recommendations
   - Manages member engagement workflows

2. **Document Agent**
   - Processes and analyzes member documents
   - Extracts key information and insights
   - Manages document verification workflows

3. **Insights Agent**
   - Analyzes member behavior and patterns
   - Generates predictive insights
   - Provides actionable recommendations

4. **Orchestration Layer**
   - Coordinates between different agents
   - Manages complex workflows
   - Ensures seamless integration of AI capabilities

## AI Capabilities

- **Natural Language Processing**
  - Text analysis and understanding
  - Sentiment analysis
  - Intent recognition
  - Contextual understanding

- **Machine Learning**
  - Member behavior prediction
  - Engagement scoring
  - Pattern recognition
  - Anomaly detection

- **Document Intelligence**
  - OCR and text extraction
  - Document classification
  - Information extraction
  - Document verification

- **Decision Support**
  - Automated recommendations
  - Risk assessment
  - Action prioritization
  - Process optimization

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 