from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class SherlockTextSplitter:
    def __init__(self, documents:list[Document]):
        self.documents = documents

    def split_documents(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,     # limit embedding model
            chunk_overlap=100,
            add_start_index=True
        )

        all_splits = text_splitter.split_documents(self.documents)
        print(f"Split chapters into {len(all_splits)} chunks.")
        return all_splits