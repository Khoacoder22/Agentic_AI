import os 
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment = os.getenv("AZURE_LLM_DEPLOYMENT")

print("Endpoint:", endpoint)
print("Deployment:", deployment)


client = OpenAI(
    api_key=api_key,
    base_url=endpoint
)

user_input = input("Enter your question: ")

response = client.responses.create(
    model=deployment,
    input=user_input
)

print(response.output_text)