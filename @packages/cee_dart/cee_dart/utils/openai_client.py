import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")       
model_name = os.getenv("AZURE_OPENAI_MODEL_NAME")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

if not subscription_key or not endpoint or not model_name or not deployment or not api_version:
    raise ValueError("AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_MODEL_NAME, AZURE_OPENAI_DEPLOYMENT, and AZURE_OPENAI_API_VERSION environment variables are not set")

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

