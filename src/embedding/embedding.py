from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


class EmbeddingGenerator:

    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            encode_kwargs={"normalize_embeddings": True},
        )
        self.vector_store = self.init_vector_store()

        

    def test_embeddings(self, documents: list[Document]):
        vector_1 = self.embeddings.embed_query(documents[0].page_content)
        vector_2 = self.embeddings.embed_query(documents[1].page_content)

        assert len(vector_1) == len(vector_2)
        print(f"Generated vectors of length {len(vector_1)}\n")
        print(vector_1[:10])

    def init_vector_store(self):
        client = QdrantClient(url="http://localhost:6333")
        vector_size = len(self.embeddings.embed_query("sample text"))

        if not client.collection_exists("test"):
            client.create_collection(
                collection_name="test",
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
        return QdrantVectorStore(
            client=client,
            collection_name="test",
            embedding=self.embeddings,
        )

    def load_docs_into_vector_store(self, document_chunks: list[Document]):
        document_ids = self.vector_store.add_documents(documents=document_chunks)
        print(document_ids[:3])

