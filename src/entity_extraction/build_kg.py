from dotenv import load_dotenv
import os
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from preprocessing.preprocessing import DocumentLoader
from splitting.splitting import SherlockTextSplitter


# Load the .env file
load_dotenv()

# Get the api key
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(temperature=0, model="gpt-5.4-nano")

graph_transformer = LLMGraphTransformer(llm=llm)

doc = DocumentLoader(file_path="../../data/chapters/chapter_1.txt")
chapter_1 = doc.load_and_clean_file()
metadata = doc.get_metadata_for_chapters([chapter_1])
docs = doc.create_documents([chapter_1], metadata)

split = SherlockTextSplitter(docs)
chunks = split.split_documents()

async def test():
    return await graph_transformer.aconvert_to_graph_documents(chunks)

graph_documents = test()
print(f"Nodes:{graph_documents[0].nodes}")
print(f"Relations:{graph_documents[0].relationships}")