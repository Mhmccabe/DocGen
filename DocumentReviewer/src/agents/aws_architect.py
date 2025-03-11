from .base_agent import BaseArchitectAgent

class AWSCloudArchitect(BaseArchitectAgent):
    """AWS Cloud Architect agent that validates cloud architecture for AWS best practices."""
    
    def __init__(self):
        system_prompt = """You are an AWS Cloud Architect responsible for reviewing documents from an AWS cloud architecture perspective.
        
        Focus on:
        - AWS Well-Architected Framework
        - Cloud service selection
        - Cost optimization
        - High availability
        - Disaster recovery
        - AWS best practices
        - Cloud security
        - Performance efficiency
        - Operational excellence
        - Service limits and quotas
        
        Provide detailed analysis with specific findings and actionable recommendations."""
        
        super().__init__("AWS Cloud Architect", system_prompt)
        
    def _extract_findings(self, response: str) -> list[str]:
        """Extract AWS-focused findings."""
        # TODO: Implement proper parsing logic
        return [
            "Evaluated AWS service selection",
            "Assessed cloud architecture patterns",
            "Analyzed cost optimization opportunities"
        ]
        
    def _extract_recommendations(self, response: str) -> list[str]:
        """Extract AWS-focused recommendations."""
        # TODO: Implement proper parsing logic
        return [
            "Optimize AWS service configuration",
            "Implement AWS Well-Architected best practices",
            "Enhance cloud cost management"
        ]
        
    def _assess_risk_level(self, response: str) -> str:
        """Assess AWS architecture risks."""
        # TODO: Implement proper risk assessment logic
        return "MEDIUM" 