from .base_agent import BaseArchitectAgent

class SolutionArchitect(BaseArchitectAgent):
    """Solution Architect agent that assesses overall solution design."""
    
    def __init__(self):
        system_prompt = """You are a Solution Architect responsible for reviewing documents from a technical solution design perspective.
        
        Focus on:
        - functional requirements are articulated
        - nonfunctional requirements are articulated
        - System architecture and design patterns
        - Component integration
        - Technical feasibility
        - Performance considerations
        - Scalability and maintainability
        - Technology stack compatibility
        - System dependencies
        - Technical debt implications
        
        Provide detailed analysis with specific findings and actionable recommendations."""
        
        super().__init__("Solution Architect", system_prompt)
        
    def _extract_findings(self, response: str) -> list[str]:
        """Extract solution design-focused findings."""
        # TODO: Implement proper parsing logic
        return [
            "Evaluated system architecture patterns",
            "Assessed component integration approach",
            "Analyzed technical feasibility and constraints"
        ]
        
    def _extract_recommendations(self, response: str) -> list[str]:
        """Extract solution-focused recommendations."""
        # TODO: Implement proper parsing logic
        return [
            "Optimize component integration strategy",
            "Implement recommended design patterns",
            "Address technical debt concerns"
        ]
        
    def _assess_risk_level(self, response: str) -> str:
        """Assess solution design risks."""
        # TODO: Implement proper risk assessment logic
        return "MEDIUM" 