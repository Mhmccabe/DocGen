from typing import Dict, List, Any, TypedDict
from langgraph.graph import Graph, StateGraph
from pydantic import BaseModel

from src.core.document_processor import Document, DocumentProcessor
from src.agents.enterprise_architect import EnterpriseArchitect
from src.agents.solution_architect import SolutionArchitect
from src.agents.infrastructure_architect import InfrastructureArchitect
from src.agents.security_architect import SecurityArchitect
from src.agents.aws_architect import AWSCloudArchitect

class ReviewState(TypedDict):
    """State object for the review workflow."""
    document: Document
    reviews: Dict[str, Any]
    final_report: Dict[str, Any]

class DocumentReviewOrchestrator:
    """Orchestrates the document review process using LangGraph."""
    
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.agents = {
            "enterprise": EnterpriseArchitect(),
            "solution": SolutionArchitect(),
            "infrastructure": InfrastructureArchitect(),
            "security": SecurityArchitect(),
            "aws": AWSCloudArchitect()
        }
        self.workflow = self._create_workflow()
        
    def _create_workflow(self) -> Graph:
        """Create the LangGraph workflow for document review."""
        
        # Create the graph
        workflow = StateGraph(ReviewState)
        
        # Add nodes for each agent
        for agent_name, agent in self.agents.items():
            workflow.add_node(agent_name, self._create_agent_node(agent))
            
        # Add aggregator node
        workflow.add_node("aggregator", self._aggregate_reviews)
        
        # Connect all agent nodes to the aggregator
        for agent_name in self.agents.keys():
            workflow.add_edge(agent_name, "aggregator")
        
        # Set all agents as entry points to run in parallel
        workflow.set_entry_points(list(self.agents.keys()))
        
        # Compile the graph
        return workflow.compile()
    
    def _create_agent_node(self, agent: Any):
        """Create a node function for an agent."""
        def node_func(state: ReviewState) -> ReviewState:
            response = agent.analyze_document(state["document"])
            # Convert AgentResponse to dict for JSON serialization
            state["reviews"][agent.name] = response.model_dump()
            return state
        return node_func
    
    def _aggregate_reviews(self, state: ReviewState) -> ReviewState:
        """Aggregate reviews from all agents into a final report."""
        final_report = {
            "document_path": state["document"].file_path,
            "overall_risk_level": self._calculate_overall_risk(state["reviews"]),
            "findings": self._aggregate_findings(state["reviews"]),
            "recommendations": self._aggregate_recommendations(state["reviews"]),
            "reviews_by_agent": state["reviews"]
        }
        state["final_report"] = final_report
        return state
    
    def _calculate_overall_risk(self, reviews: Dict) -> str:
        """Calculate overall risk level based on individual agent assessments."""
        risk_levels = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
        risk_scores = [risk_levels[review["risk_level"]] for review in reviews.values()]
        avg_risk = sum(risk_scores) / len(risk_scores)
        
        if avg_risk >= 2.5:
            return "HIGH"
        elif avg_risk >= 1.5:
            return "MEDIUM"
        return "LOW"
    
    def _aggregate_findings(self, reviews: Dict) -> List[str]:
        """Aggregate findings from all agents."""
        findings = []
        for agent_name, review in reviews.items():
            findings.extend([f"[{agent_name}] {finding}" for finding in review["findings"]])
        return findings
    
    def _aggregate_recommendations(self, reviews: Dict) -> List[str]:
        """Aggregate recommendations from all agents."""
        recommendations = []
        for agent_name, review in reviews.items():
            recommendations.extend([f"[{agent_name}] {rec}" for rec in review["recommendations"]])
        return recommendations
    
    def review_document(self, file_path: str) -> Dict:
        """
        Process and review a document using the agent workflow.
        
        Args:
            file_path: Path to the document file (PDF or DOCX)
            
        Returns:
            Dict containing the final consolidated review report
        """
        # Load and process the document
        document = self.document_processor.load_document(file_path)
        
        # Initialize the workflow state
        initial_state: ReviewState = {
            "document": document,
            "reviews": {},
            "final_report": {}
        }
        
        # Execute the workflow
        final_state = self.workflow.invoke(initial_state)
        
        return final_state["final_report"] 