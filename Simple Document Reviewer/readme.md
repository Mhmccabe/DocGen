
## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/yourrepository.git
    ```

2. Navigate to the project directory:
    ```sh
    cd yourrepository
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. Copy the example environment file and update it with your API keys:
    ```sh
    cp Simple\ Document\ Reviewer/example\ .env .env
    ```

2. Edit the `.env` file with your API keys:
    ```env
    OPENAI_API_KEY = "sk-YOUR KEY HERE"
    OPENAI_MODEL="gpt-4-turbo-preview"
    OPENAI_TEMPERATURE="0.3"
    OPENAI_MAX_TOKENS="2000"

    ANTHROPIC_API_KEY = "sk-YOUR KEY HERE"
    ANTHROPIC_MODEL="claude-3-5-sonnet-20240620"
    ANTHROPIC_TEMPERATURE="0.3"
    ANTHROPIC_MAX_TOKENS="2000" 

    LLM_PROVIDER="anthropic"
    ```

## Usage

1. Run the main script to start the document review process:
    ```sh
    python DocumentReviewer/src/main.py
    ```


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

