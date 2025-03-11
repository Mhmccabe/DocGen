from typing import Dict, Any
import os
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from src.core.document_processor import Document

class AgentResponse(BaseModel):
    """Structured response from an agent's review."""
    agent_name: str
    findings: list[str]
    recommendations: list[str]
    risk_level: str
    confidence_score: float

class BaseArchitectAgent:
    """Base class for all architect agents in the system."""
    
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "4000"))
        )
        
    def analyze_document(self, document: Document) -> AgentResponse:
        """
        Analyze the document and return structured findings.
        
        Args:
            document: The Document object containing the content to analyze.
            
        Returns:
            AgentResponse containing the analysis results.
        """
        print(f"Analyzing document with {self.name} agent...")
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"Please analyze the following document from your perspective as {self.name}:\n\n{document.content}")
        ]
        
        response = self.llm.invoke(messages)
        
        # Process the response into structured format
        # This is a simplified version - in practice, you'd want to prompt
        # the LLM to return structured data that can be easily parsed
        return AgentResponse(
            agent_name=self.name,
            findings=self._extract_findings(response.content),
            recommendations=self._extract_recommendations(response.content),
            risk_level=self._assess_risk_level(response.content),
            confidence_score=0.85  # This would be dynamically calculated in practice
        )
    
    def _extract_findings(self, response: str) -> list[str]:
        """Extract key findings from the LLM response."""
        # In practice, you'd want to implement proper parsing logic
        return ["Finding 1", "Finding 2"]  # Placeholder
        
    def _extract_recommendations(self, response: str) -> list[str]:
        """Extract recommendations from the LLM response."""
        # In practice, you'd want to implement proper parsing logic
        return ["Recommendation 1", "Recommendation 2"]  # Placeholder
        
    def _assess_risk_level(self, response: str) -> str:
        """Assess the overall risk level based on the analysis."""
        # In practice, you'd want to implement proper risk assessment logic
        return "MEDIUM"  # Placeholder 