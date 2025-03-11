from .base_agent import BaseArchitectAgent

class EnterpriseArchitect(BaseArchitectAgent):
    """Enterprise Architect agent that reviews business alignment and strategic fit."""
    
    def __init__(self):
        system_prompt = """You are an Enterprise Architect responsible for reviewing documents from a business alignment and strategic fit perspective.
        
        Focus on:
        - clear technical landscape management
        - Business strategy alignment
        - Value proposition is clearly articulated
        - Stakeholders and impact is described
        - Business process integration
        - ROI and business case
        - Enterprise architecture principles
        - Business capability mapping
        - Strategic roadmap alignment
        
        Provide detailed analysis with specific findings and actionable recommendations."""
        
        super().__init__("Enterprise Architect", system_prompt)
        
    def _extract_findings(self, response: str) -> list[str]:
        """Extract business and strategy-focused findings."""
        # TODO: Implement proper parsing logic
        return [
            "Analyzed business strategy alignment",
            "Evaluated stakeholder impact",
            "Assessed enterprise architecture compliance"
        ]
        
    def _extract_recommendations(self, response: str) -> list[str]:
        """Extract business-focused recommendations."""
        # TODO: Implement proper parsing logic
        return [
            "Enhance business process integration",
            "Strengthen alignment with enterprise architecture principles",
            "Update strategic roadmap"
        ]
        
    def _assess_risk_level(self, response: str) -> str:
        """Assess business and strategic risks."""
        # TODO: Implement proper risk assessment logic
        return "LOW" 