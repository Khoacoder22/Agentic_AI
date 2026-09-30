import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI( api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                 base_url=(os.getenv("AZURE_OPENAI_ENDPOINT")))

LLM_DEPLOYMENT = os.getenv("AZURE_LLM_DEPLOYMENT")

def ask_llm(prompt: str) -> str:
    response = client.responses.create(
        model=LLM_DEPLOYMENT,
        input=prompt
    )
    return response.output_text