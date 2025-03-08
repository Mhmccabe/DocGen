from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.tools import DuckDuckGoSearchRun
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

class WebSearchAgent:
    def __init__(self, temperature=0.7):
        # Initialize the language model
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=temperature
        )
        
        # Initialize the search tool
        self.search_tool = DuckDuckGoSearchRun()
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Initialize the agent
        self.agent = initialize_agent(
            tools=[self.search_tool],
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3
        )

    def search(self, query: str) -> str:
        """
        Perform a web search and return the answer
        """
        try:
            response = self.agent.invoke({"input": query})
            return response["output"]
        except Exception as e:
            return f"An error occurred: {str(e)}"

def main():
    print("Web Search Agent (Type 'quit' to exit)")
    print("-" * 50)
    
    # Initialize the agent
    agent = WebSearchAgent()
    
    while True:
        # Get user input
        query = input("\nEnter your question: ").strip()
        
        # Check for exit command
        if query.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            sys.exit(0)
        
        # Check for empty input
        if not query:
            print("Please enter a question to search.")
            continue
        
        # Perform search
        print("\nSearching and analyzing...")
        try:
            response = agent.search(query)
            print("\nAnswer:")
            print("-" * 50)
            print(response)
            print("-" * 50)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 
    