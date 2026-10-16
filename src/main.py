import os
import postgres
from langchain_core.documents import Document

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_postgres import PGVector
from dotenv import load_dotenv

load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)

vs = PGVector(
    embeddings=embeddings,
    embedding_length=384,
    collection_name="Assistant",
    connection=f"postgresql://{os.getenv('SQL_USER')}:{os.getenv('SQL_PASS')}@{os.getenv('SQL_ADDRESS')}:5432/rag"
)

retriever = vs.as_retriever()

llm = ChatOpenAI(model=os.getenv("MODEL_NAME", ""), base_url=os.getenv("PROVIDER_URL"), api_key=os.getenv("PROVIDER_KEY"))

agent = create_agent(llm, [retriever.as_tool(name="retrieve_context", description="Retrieve context based on the current conversation")])

resp = agent.invoke({'messages': [{'role': 'user', 'content': f"Hello, who is Lucachinou? And what his specialisation?"}]})
print(resp.get("messages")[-1].content)