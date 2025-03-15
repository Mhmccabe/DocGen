# main.py
import sys
import os
import argparse
from document_loader import load_document, convert_to_markdown
from review_documentation import review_document
from config import LLM_PROVIDER


def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Review a document using AI models')
    parser.add_argument('document_file', help='Path to the document file to review')
    
    args = parser.parse_args()

    try:
        # Try to load and process the document
        text = load_document(args.document_file)
        markdown_text = convert_to_markdown(text)
        print(f"Successfully loaded and converted document: {args.document_file}")
        print(f"Using {LLM_PROVIDER.upper()} as the language model provider\n")

        reviews, improvements = review_document(markdown_text, model_provider=LLM_PROVIDER)
        
        if reviews is None or improvements is None:
            print("Document review failed. Please check the error messages above.")
            sys.exit(1)

        print("\n=== Individual Reviews ===")
        for perspective, review in reviews.items():
            print(f"\n--- {perspective} Review ---")
            print(review)

        print("\n=== Consolidated Improvements ===")
        print(improvements)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please check if the file exists and the path is correct.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        print("Supported file types are: .pdf, .doc, .docx")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
