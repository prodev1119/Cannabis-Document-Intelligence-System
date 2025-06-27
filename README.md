# Cannabis Document Intelligence System

A comprehensive document classification system that analyzes municipal documents for cannabis business relevance and executes automation workflows based on priority levels.

## 🌿 Overview

This system implements the exact scoring methodology specified in the cannabis automation platform test requirements:

- **Document Analysis**: Classifies municipal documents using weighted keyword scoring
- **Automation Workflows**: Executes appropriate actions based on priority levels
- **Business Intelligence**: Provides actionable insights for cannabis business opportunities

## 🚀 Features

### Document Classification
- **High Value Keywords** (10 points each): "cannabis retail", "dispensary license", "application window", etc.
- **Medium Value Keywords** (5 points each): "public hearing", "planning commission", "draft ordinance", etc.
- **Low Value Keywords** (2 points each): "cannabis", "marijuana", "dispensary", "retail", etc.
- **Context Modifiers**: Positive/negative modifiers, date bonuses, title/heading bonuses
- **Smart Scoring**: Thresholds for HIGH/MEDIUM/LOW/IRRELEVANT classifications

### Automation Workflows
- **HIGH PRIORITY**: Immediate Slack alerts with detailed information
- **MEDIUM PRIORITY**: Weekly digest emails for planning purposes
- **LOW PRIORITY**: JSON logging for future reference
- **IRRELEVANT**: No action taken

### Technical Features
- **FastAPI Web Interface**: REST API with interactive documentation
- **Comprehensive Testing**: Real municipal documents from the `docs` folder
- **Export Capabilities**: JSON, text reports, and detailed logs
- **Methodology Documentation**: Transparent scoring system explanation

## 📋 Requirements

```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Quick Start

### 1. Run the Complete System
```bash
python main.py
```

This will:
- Process all real municipal documents in the `docs` folder
- Classify each document for cannabis business relevance
- Execute automation workflows
- Generate comprehensive reports
- Save results to multiple files

### 2. Start the Web API
```bash
python api.py
```

Then visit:
- **API Documentation**: http://localhost:8000/docs
- **Web Interface**: http://localhost:8000

### 3. Test Individual Components
```bash
# Test the classifier directly
python -c "
from cannabis_classifier import CannabisDocumentClassifier
import os

def load_real_documents(folder_path='docs'):
    documents = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    documents[file] = f.read()
    return documents

classifier = CannabisDocumentClassifier()
documents = load_real_documents()
results = classifier.process_documents(documents)

for result in results:
    print(f'{result.document_name}: {result.classification.value} (Score: {result.score})')
"
```

## 📊 Sample Results

The system processes all municipal documents in the `docs` folder and typically produces:

- **High Priority**: Documents requiring immediate action
- **Medium Priority**: Documents to monitor and plan
- **Low Priority**: Background awareness
- **Irrelevant**: No action needed

### Example High Priority Document
```
🔴 city_cannabis_ordinance.txt
   Score: 85 | Classification: HIGH_PRIORITY
   Reasoning: Found key phrases: cannabis retail, ordinance approved, application window; Recent dates detected (+5 points); Keywords in headings (+2 points)
   Key Phrases: cannabis retail, ordinance approved, application window
```

## 🏗️ System Architecture

### Core Components

1. **`cannabis_classifier.py`**
   - Main classification engine
   - Scoring system implementation
   - Date extraction and analysis
   - Title/heading bonus detection

2. **`automation_workflows.py`**
   - Slack alert generation
   - Email digest creation
   - JSON logging system
   - Workflow orchestration

3. **`main.py`**
   - Complete system orchestration
   - Report generation
   - File export functionality

4. **`api.py`**
   - FastAPI web interface
   - REST API endpoints
   - Interactive documentation

### File Structure
```
cannabis-document-intelligence/
├── cannabis_classifier.py      # Core classification engine
├── automation_workflows.py     # Automation workflows
├── main.py                     # Main application
├── api.py                      # FastAPI web interface
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── docs/                       # Real municipal documents
```

## 🔧 API Endpoints

### Web Interface
- `GET /` - API documentation and overview
- `GET /docs` - Interactive Swagger UI documentation

### Document Classification
- `POST /classify` - Classify a single document
- `POST /classify-batch` - Classify multiple documents
- `POST /upload-file` - Upload and classify a text file

### Information
- `GET /methodology` - Get detailed methodology explanation

### Automation
- `POST /automation-workflows` - Execute automation workflows

## 📈 Methodology

### Scoring System

**High Value Keywords (10 points each):**
- "cannabis retail", "dispensary license", "application window"
- "ordinance approved", "licensing program", "application period"
- "merit-based selection", "conditional use permit approved", "second reading"

**Medium Value Keywords (5 points each):**
- "public hearing", "planning commission", "draft ordinance"
- "zoning amendment", "social equity", "moratorium lifted"
- "cannabis business", "study session"

**Low Value Keywords (2 points each):**
- "cannabis", "marijuana", "dispensary", "retail"
- "tax revenue", "budget discussion", "general mention"

### Context Modifiers
- **Positive Modifiers** (+3 points): "approved", "passed", "effective", "final"
- **Negative Modifiers** (-3 points): "prohibited", "banned", "rejected"
- **Date Bonus** (+5 points): Dates within 90 days
- **Title/Heading Bonus** (+2 points): Keywords in document titles/headings

### Classification Thresholds
- **70+ points**: HIGH PRIORITY (immediate action needed)
- **30-69 points**: MEDIUM PRIORITY (monitor and plan)
- **10-29 points**: LOW PRIORITY (background awareness)
- **Under 10 points**: IRRELEVANT (ignore)

## 📁 Generated Files

After running the system, the following files are generated:

- `classification_results.json` - Detailed classification data
- `automation_results.json` - Workflow execution details
- `summary_report.txt` - Human-readable summary
- `automation_report.txt` - Automation workflow report
- `methodology.txt` - Detailed methodology explanation
- `automation_log.json` - Low priority document log

## 🧪 Testing

### Real Documents Included
- All municipal documents in the `docs` folder are processed.

### Running Tests
```bash
# Run complete analysis
python main.py

# Test API endpoints
python api.py
# Then visit http://localhost:8000/docs
```

## 🎯 Business Logic

The system is designed to identify documents that represent:

1. **Immediate Business Opportunities**
   - Approved ordinances creating new markets
   - Active licensing programs with application windows
   - Recent regulatory changes

2. **Monitoring Requirements**
   - Ongoing regulatory processes
   - Potential future opportunities
   - Policy discussions requiring attention

3. **Background Intelligence**
   - General cannabis-related activities
   - Market trends and developments
   - Historical context

## 🔄 Automation Workflows

### High Priority Documents
- **Action**: Immediate Slack alerts
- **Content**: Document details, score, reasoning, key phrases
- **Purpose**: Enable immediate follow-up and action

### Medium Priority Documents
- **Action**: Weekly digest emails
- **Content**: Summarized information for planning
- **Purpose**: Support strategic planning and monitoring

### Low Priority Documents
- **Action**: JSON logging
- **Content**: Structured data for future reference
- **Purpose**: Maintain historical record and background intelligence

## 🚀 Deployment

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the system
python main.py

# Start API server
python api.py
```

### Production Deployment
```bash
# Using uvicorn for production
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4

# Using gunicorn
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📝 Customization

### Adding New Keywords
Edit `cannabis_classifier.py` to add new keywords to the appropriate categories:

```python
self.high_value_keywords.append("new high value phrase")
self.medium_value_keywords.append("new medium value phrase")
self.low_value_keywords.append("new low value phrase")
```

### Modifying Scoring
Adjust thresholds in `cannabis_classifier.py`:

```python
self.thresholds = {
    PriorityLevel.HIGH_PRIORITY: 75,  # Changed from 70
    PriorityLevel.MEDIUM_PRIORITY: 35,  # Changed from 30
    PriorityLevel.LOW_PRIORITY: 15   # Changed from 10
}
```

### Custom Automation Workflows
Extend `automation_workflows.py` to add new automation actions:

```python
def custom_workflow(self, result: ClassificationResult):
    # Implement custom automation logic
    pass
```

## 🤝 Contributing

This system is designed for the cannabis automation platform test. The methodology and scoring system are based on the specific requirements provided in the test instructions.

## 📄 License

This project is created for the cannabis automation platform skills assessment.

---

**Built for Cannabis Business Intelligence** 🌿 