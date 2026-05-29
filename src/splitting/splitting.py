from langchain_text_splitters import RecursiveCharacterTextSplitter

class SherlockTextSplitter():
    def __init__(self, documents):
        self.documents = documents

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=150,
        add_start_index=True
    )

    all_splitter = text_splitter.splitpass_documents