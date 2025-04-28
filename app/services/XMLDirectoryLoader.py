from pathlib import Path
from langchain.schema import Document
from typing import List
import xml.etree.ElementTree as ET


class XMLDirectoryLoader:
    """
    • A custom loader you wrote to read all XML files inside a directory and return them as LangChain Document objects.
    • Goal: load .xml files so that downstream processes (like RAG pipelines) can treat XMLs like normal text documents.
    """
    def __init__(self, directory_path: str):
        self.directory_path = Path(directory_path)

    def load(self) -> List[Document]:
        documents = []
        for xml_file in self.directory_path.glob("*.xml"):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                text = ET.tostring(root, encoding="utf-8", method="text").decode(
                    "utf-8"
                )

                documents.append(
                    Document(page_content=text, metadata={"source": xml_file.name})
                )
            except Exception as e:
                print(f"⚠️ Skipping {xml_file.name}: {e}")
        return documents
