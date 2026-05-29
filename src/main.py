from preprocessing.preprocessing import DocumentLoader

doc = DocumentLoader("../../data/raw/holmes_raw.txt")
clean_file = doc.load_and_clean_file()
chapters = doc.split_text_into_chapters(clean_file)
md = doc.get_metadata_for_chapters(chapters)

