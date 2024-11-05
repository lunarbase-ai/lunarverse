from typing import Dict, Optional
from html.parser import HTMLParser
from pydantic import BaseModel, HttpUrl, RootModel, ValidationError

class HTMLContentModel(BaseModel):
    text: Optional[str] = None
    content: str

class HTMLContentMapperModel(RootModel[Dict[HttpUrl, HTMLContentModel]]):
    pass


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_text(self):
        content = ' '.join(self.text)

        self._clean_text()
        
        return content
    
    def _clean_text(self):
        self.text = []
    

class HTMLTextExtractor:
    def __init__(self):
        self.parser = TextParser()

    def extract(self, html_content_mapper: HTMLContentMapperModel) -> HTMLContentMapperModel:
        try:
            html_content_mapper = HTMLContentMapperModel(html_content_mapper)
        except ValidationError as e:
            raise ValueError(f"Invalid Html content mapper: {e}")

        results: HTMLContentMapperModel = {}

        for url, data in html_content_mapper.model_dump().items():
            self.parser.feed(data["content"])
            results[url] = {
                "content": data["content"],
                "text": self.parser.get_text()
            }

        return results