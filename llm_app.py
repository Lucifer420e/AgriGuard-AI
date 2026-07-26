import os
from dotenv import load_dotenv

# .env file se API Key load karega
load_dotenv()

def llm_app(topic):
    from langchain_core.prompts import PromptTemplate
    from langchain_groq import ChatGroq

    # 1. Initialize your LLM using .env variable
    groq_api = os.getenv("GROQ_API_KEY")
    
    llm = ChatGroq(model='openai/gpt-oss-120b', api_key=groq_api, temperature=0.1)

    prompt = PromptTemplate(
        input_variables=['topic'],
        template='You are an agriculture expert.\nprovide five important lines covering about {topic}.'
    )

    chain = prompt | llm
    return chain.invoke(topic)