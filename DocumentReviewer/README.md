# Document Review System

A LangGraph-based multi-agent system for comprehensive document review and analysis. The system processes documents (PDF or DOCX) and provides detailed feedback from multiple architectural perspectives.

## Features

- Multi-agent document analysis using LangGraph orchestration
- Support for PDF and DOCX document formats
- Comprehensive review from five different architectural perspectives:
  - Enterprise Architecture
  - Solution Architecture
  - Infrastructure Architecture
  - Security Architecture
  - AWS Cloud Architecture
- Consolidated feedback report with findings and recommendations
- Risk assessment and scoring
- JSON report generation
- Command-line interface for easy document processing

## Architecture

The system consists of the following components:

- Document Processor: Handles document loading and text extraction
- Architect Agents: Specialized agents for different review perspectives
- LangGraph Orchestrator: Coordinates the review workflow
- Report Generator: Consolidates findings and generates the final report

## Prerequisites

- Python 3.8+
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd document-reviewer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with your configuration:
```bash
# Required
OPENAI_API_KEY=your-api-key-here

# Optional - LLM Configuration
OPENAI_MODEL=gpt-4-turbo-preview  # Default model
OPENAI_TEMPERATURE=0.7            # Controls randomness (0.0 to 1.0)
OPENAI_MAX_TOKENS=4000           # Maximum tokens per response
```

## Usage

1. Command-line interface:
```bash
# Basic usage
python analyse.py path/to/your/document.pdf

# Specify custom output location
python run.py path/to/your/document.docx -o /path/to/output/report.json
```

The script accepts the following arguments:
- `file_path`: Path to the document file (PDF or DOCX) to analyze (required)
- `-o, --output`: Custom output path for the JSON report (optional)

2. Programmatic usage:
```python
from src.core.orchestrator import DocumentReviewOrchestrator

# Initialize the orchestrator
orchestrator = DocumentReviewOrchestrator()

# Review a document
report = orchestrator.review_document("path/to/your/document.pdf")
```

## Output

The system generates a comprehensive review report including:
- Overall risk assessment
- Findings from each architectural perspective
- Specific recommendations
- Detailed analysis from each agent

The report is both printed to the console and saved as a JSON file.

## Agent Descriptions

### Enterprise Architect
Reviews business alignment and strategic fit, focusing on:
- Business strategy alignment
- Value proposition
- Stakeholder impact
- Business process integration

### Solution Architect
Assesses overall solution design, focusing on:
- System architecture
- Component integration
- Technical feasibility
- Performance considerations

### Infrastructure Architect
Evaluates infrastructure requirements, focusing on:
- Hardware requirements
- Network architecture
- System capacity
- Operational requirements

### Security Architect
Checks security and compliance, focusing on:
- Security requirements
- Compliance standards
- Data protection
- Risk mitigation

### AWS Cloud Architect
Validates cloud architecture, focusing on:
- AWS Well-Architected Framework
- Cloud service selection
- Cost optimization
- High availability

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 