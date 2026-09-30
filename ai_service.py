from typing import Dict, Any

class AIService:
    """Provider-agnostic AI layer.

    Replace demo_generate() with your chosen LLM provider implementation.
    """

    async def generate_document(self, document_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Demo mode keeps the project runnable without an API key.
        title = document_type.replace("_", " ").title()
        sections = [
            {
                "heading": "1. Parties",
                "content": f"This {title} is prepared for the parties identified in the supplied information."
            },
            {
                "heading": "2. Purpose",
                "content": "The parties intend to establish the terms described in the user-provided information."
            },
            {
                "heading": "3. Terms",
                "content": "The specific terms should be completed from the supplied information and reviewed before use."
            },
            {
                "heading": "4. Governing Law",
                "content": "Governing law should be specified by the user and reviewed for the applicable jurisdiction."
            },
            {
                "heading": "5. Signatures",
                "content": "Party 1: ____________________\n\nParty 2: ____________________"
            }
        ]
        return {
            "title": title,
            "sections": sections,
            "terms": [{"term": k, "value": str(v)} for k, v in data.items()]
        }

ai_service = AIService()
