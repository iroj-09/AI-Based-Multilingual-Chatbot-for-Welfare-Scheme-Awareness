from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv

load_dotenv()
import os

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# llm = HuggingFaceEndpoint(
#     repo_id = "meta-llama/Llama-3.1-8B-Instruct",
#     task = "text-generation",
#     huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
# )

# model = ChatHuggingFace(
#     llm=llm)

def generate_answer(prompt):

    response = model.invoke(prompt)

    return response.content

def normalize_query(query: str):

    prompt = f"""
You are a language normalization assistant.

Convert the following query into clear English.

The query may be:
- English
- Hindi
- Hinglish
- Mixed Hindi and English

Return ONLY the normalized English query.

Query:
{query}
"""

    response = model.invoke(prompt)

    return response.content.strip()