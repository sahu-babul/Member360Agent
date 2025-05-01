import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
import os
from dotenv import load_dotenv

load_dotenv()

class SemanticKernelSetup:
    def __init__(self):
        self.kernel = sk.Kernel()
        
        # Configure Azure OpenAI
        self.kernel.add_chat_service(
            "chat_completion",
            AzureChatCompletion(
                deployment_name="gpt-4",
                endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                api_version="2023-07-01-preview"
            )
        )
        
        # Import skills
        self.import_skills()
    
    def import_skills(self):
        # Member analysis skill
        member_analysis = """
        Analyze the member's profile and provide insights about:
        - Membership status and history
        - Interaction patterns
        - Document status
        - Potential engagement opportunities
        """
        
        self.kernel.import_semantic_skill_from_directory(
            "skills",
            "member_analysis",
            member_analysis
        )
        
        # Document processing skill
        document_processing = """
        Process and analyze member documents to:
        - Extract key information
        - Verify document authenticity
        - Identify important dates and terms
        - Flag any potential issues
        """
        
        self.kernel.import_semantic_skill_from_directory(
            "skills",
            "document_processing",
            document_processing
        )
        
        # Interaction recommendation skill
        interaction_recommendation = """
        Generate recommendations for member interactions based on:
        - Member history
        - Current status
        - Recent activities
        - Business goals
        """
        
        self.kernel.import_semantic_skill_from_directory(
            "skills",
            "interaction_recommendation",
            interaction_recommendation
        )
    
    async def analyze_member(self, member_data):
        """Analyze member profile using semantic kernel"""
        context = self.kernel.create_new_context()
        context["member_data"] = member_data
        
        result = await self.kernel.run_async(
            context,
            "member_analysis"
        )
        
        return result
    
    async def process_document(self, document_data):
        """Process document using semantic kernel"""
        context = self.kernel.create_new_context()
        context["document_data"] = document_data
        
        result = await self.kernel.run_async(
            context,
            "document_processing"
        )
        
        return result
    
    async def generate_recommendations(self, member_id):
        """Generate interaction recommendations using semantic kernel"""
        context = self.kernel.create_new_context()
        context["member_id"] = member_id
        
        result = await self.kernel.run_async(
            context,
            "interaction_recommendation"
        )
        
        return result 