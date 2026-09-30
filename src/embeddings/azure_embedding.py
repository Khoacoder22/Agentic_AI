import os 
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# chunk -> create_embedding() -> [0.012, -0.032]
client = OpenAI(
    api_key= os.getenv("AZURE_OPENAI_API_KEY"),
    base_url= os.getenv("AZURE_OPENAI_ENDPOINT")
)

EMBEDDING_MODEL = os.getenv("AZURE_EMBEDDING_DEPLOYMENT")

def create_embedding(text: str): 

    response = client.embeddings.create(
        model = EMBEDDING_MODEL,
        input = text
    )

    return response.data[0].embedding