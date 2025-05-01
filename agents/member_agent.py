from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
import os
from dotenv import load_dotenv

load_dotenv()

# Load LLM configuration
config_list = [
    {
        "model": "gpt-4",
        "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
        "base_url": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "api_type": "azure",
        "api_version": "2023-07-01-preview"
    }
]

# Create agents
member_assistant = AssistantAgent(
    name="member_assistant",
    llm_config={"config_list": config_list},
    system_message="""You are a helpful assistant specialized in member management.
    You can help with:
    - Member profile analysis
    - Interaction recommendations
    - Document processing
    - Member engagement strategies
    """
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "workspace"},
    llm_config={"config_list": config_list}
)

def analyze_member_profile(member_data):
    """Analyze member profile and provide insights"""
    user_proxy.initiate_chat(
        member_assistant,
        message=f"Analyze this member profile and provide insights: {member_data}"
    )

def process_document(document_data):
    """Process member document and extract relevant information"""
    user_proxy.initiate_chat(
        member_assistant,
        message=f"Process this document and extract relevant information: {document_data}"
    )

def generate_interaction_recommendations(member_id):
    """Generate recommendations for member interactions"""
    user_proxy.initiate_chat(
        member_assistant,
        message=f"Generate interaction recommendations for member ID: {member_id}"
    ) 