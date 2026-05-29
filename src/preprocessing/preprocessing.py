import re
from pydantic import BaseModel
from langchain_core.documents import Document


class StoryMetadata(BaseModel):
    story_id: str
    story_title: str
    order_in_collection: int
    source_url: str
    char_count: int


class DocumentLoader:
    STORY_START_MARKER = re.compile(r"(?=I. A SCANDAL IN BOHEMIA)")
    STORY_END_MARKER = re.compile(r"\*\*\*\s(?:[A-Z]|[ \n])*\*\*\*", re.MULTILINE)
    CHAPTER_START_MARKER = re.compile(
        r"(?=\n(?:[IXV]{1,4}\.\s+[A-Z][A-Z\’\- ]*)\n{2,})", re.MULTILINE
    )

    # CHAPTER_START_MARKER = re.compile(r"(?=([IVX]{1,3}\.(\s[A-Z]+){1,}\n\n))")
    TITLE_MARKER = re.compile(r"([A-Z][A-Z\’\- ]*)\n{2,}", re.MULTILINE)
    # ILLUSTRATION_MARKER = re.compile(r"\[Illustration:\s.+]")
    SUBCHAPTER_START_MARKER = re.compile(r"(?=\n\n([IV]+))", re.MULTILINE)

    source_url = "https://www.gutenberg.org/files/1661/1661-0.txt"

    def __init__(self, file_path):
        self.file_path = file_path

    def load_and_clean_file(self):
        with open(self.file_path) as file:
            raw_file = file.read()

            # remove boilerplate text
            text_without_pre = re.split(self.STORY_START_MARKER, raw_file)[1]
            text_without_suc = re.split(self.STORY_END_MARKER, text_without_pre)[0]
            return text_without_suc

    def split_text_into_chapters(self, text):
        # split into chapters
        return re.split(self.CHAPTER_START_MARKER, text)

    def get_metadata_for_chapters(self, chapters: list[str]):
        metadata_objects: dict[int, StoryMetadata] = {}

        for i in range(len(chapters)):
            # get titles
            title_match = re.search(self.TITLE_MARKER, chapters[i])
            metadata = StoryMetadata(
                story_id=f"1661_story_{i+1}",
                raw_char_count=len(chapters[i]),
                source_url=self.source_url,
                order_in_collection=i + 1,
                story_title=title_match.group(1),
                char_count=len(chapters[i]),
            )
            # print(metadata)
            metadata_objects[i] = metadata

        return metadata_objects

    def save_chapters(self, chapters: list[str]):
        for i in range(len(chapters)):
            with open(f"../../data/chapters/chapter_{i+1}", "w") as f:
                f.write(chapters[i])

    def create_document(
        self, chapters: list[str], chapter_metadata: dict[int, StoryMetadata]
    ):
        documents: list[Document] = []
        for i in range(len(chapters)):
            documents.append(
                Document(page_content=chapters[i], metadata=chapter_metadata.get(i))
            )
        return documents

    # def remove_illustrations(self, text: str):
    #     return re.sub(self.ILLUSTRATION_MARKER, "", text)

    # def split_chapters(self, text: str):
    #     return re.split(self.CHAPTER_START_MARKER, text)[1:]

    # def extract_chapter_info(self, chapters: list[str]):
    #     titles: dict = {}
    #     for i in range(len(chapters)):
    #         match = re.search(self.TITLE_MARKER, chapters[i])
    #         titles[i + 1] = match.group(1)

    #     return titles


doc = DocumentLoader("../../data/raw/holmes_raw.txt")
clean_file = doc.load_and_clean_file()
chapters = doc.split_text_into_chapters(clean_file)
md = doc.get_metadata_for_chapters(chapters)
doc.save_chapters(chapters)
print(md.get(1))
# print(metadata.keys())
# with open("./out.txt", "w") as f:
#      f.write(metadata[0])
