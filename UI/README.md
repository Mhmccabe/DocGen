# AI Document Generator

This Streamlit application uses LangChain and OpenAI to generate and improve document content based on markdown outlines. The application features a split-screen interface where users can input their document outline on the left side and view the generated content with suggested improvements on the right side.

## Features

- Split-screen interface for easy document outline input and content viewing
- Markdown-based outline format
- AI-powered content generation using OpenAI's GPT-4
- Automatic content review and improvement suggestions
- Expandable sections for viewing improvement suggestions

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run main.py
   ```
2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)
3. Enter your document outline in the left panel using markdown headers (#) to separate sections
4. Click "Generate Content" to create content for each section
5. View the generated content and improvement suggestions in the right panel

## Example Outline Format

```markdown
# Introduction
Brief overview of the topic

# Main Points
Key points to cover

# Conclusion
Summary and next steps
```

## Requirements

- Python 3.8+
- OpenAI API key
- Required Python packages (listed in requirements.txt) 