from typing import Optional


class Ebook:
    def __init__(self,
                 title: str,
                 topic: str,
                 target_audience: str,
                 docx_file: str,
                 pdf_file: Optional[str] = None,
                 ):
        self.title = title
        self.topic = topic
        self.target_audience = target_audience
        self.docx_file = docx_file
        self.pdf_file = pdf_file
        # self._cover_img = cover_img
        # self._assets = assets
        # self._page_count = page_count
