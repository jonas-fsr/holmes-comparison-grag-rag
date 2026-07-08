from preprocessing.preprocessing import DocumentLoader
from splitting.splitting import SherlockTextSplitter
from embedding.embedding import EmbeddingGenerator

doc = DocumentLoader("../data/raw/holmes_raw.txt")
clean_file = doc.load_and_clean_file()
chapters = doc.split_text_into_chapters(clean_file)
# subchapters = doc.extract_subchapters(chapters)
# doc.save_chapters(subchapters)
metadata = doc.get_metadata_for_chapters(chapters)
docs = doc.create_documents(chapters, metadata)

split = SherlockTextSplitter(docs)
chunks = split.split_documents()

emb = EmbeddingGenerator()
emb.load_docs_into_vector_store(chunks)
