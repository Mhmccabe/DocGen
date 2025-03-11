import os
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv
from src.core.orchestrator import DocumentReviewOrchestrator

def validate_file_path(file_path: str) -> str:
    """Validate that the file exists and is of supported type."""
    path = Path(file_path)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"File not found: {file_path}")
    if path.suffix.lower() not in ['.pdf', '.docx']:
        raise argparse.ArgumentTypeError(f"Unsupported file type: {path.suffix}. Only PDF and DOCX files are supported.")
    return str(path.absolute())

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Document Review System - Analyze documents using multiple architectural perspectives"
    )
    parser.add_argument(
        "file_path",
        type=validate_file_path,
        help="Path to the document file (PDF or DOCX) to analyze"
    )
    parser.add_argument(
        "-o", "--output",
        help="Custom output path for the JSON report (default: input_file_review_report.json)",
        type=str
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Load environment variables (for OpenAI API key)
    load_dotenv()
    
    # Initialize the orchestrator
    orchestrator = DocumentReviewOrchestrator()
    
    try:
        # Review the document
        print(f"\nAnalyzing document: {args.file_path}")
        print("This may take a few minutes depending on the document size...\n")
        
        review_report = orchestrator.review_document(args.file_path)
        
        # Print the report in a formatted way
        print("\n=== Document Review Report ===")
        print(f"\nDocument: {review_report['document_path']}")
        print(f"Overall Risk Level: {review_report['overall_risk_level']}")
        
        print("\nKey Findings:")
        for finding in review_report['findings']:
            print(f"- {finding}")
            
        print("\nRecommendations:")
        for recommendation in review_report['recommendations']:
            print(f"- {recommendation}")
            
        # Determine output path
        if args.output:
            output_path = args.output
        else:
            input_path = Path(args.file_path)
            output_path = str(input_path.parent / f"{input_path.stem}_review_report.json")
        
        # Save the report to a JSON file
        with open(output_path, 'w') as f:
            json.dump(review_report, f, indent=2)
        print(f"\nDetailed report saved to: {output_path}")
        
    except Exception as e:
        print(f"Error during document review: {str(e)}")
        parser.exit(1)

if __name__ == "__main__":
    main() 