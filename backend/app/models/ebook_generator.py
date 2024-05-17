from backend.app.models.langchain_wrapper import LangchainWrapper
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm


class EbookGenerator:
    def __init__(self):
        self.langchain_wrapper = LangchainWrapper()

    def generate_title(self, topic: str, target_audience: str) -> str:
        print("starting generate title")
        title_prompt = (
            f'We are writing an eBook. It is about "{topic}". Our'
            f' reader is:  "{target_audience}". Write a short, catch'
            " title clearly directed at our reader that is less than"
            " 9 words and proposes a “big promise” that will be sure to grab"
            " the readers attention."
        )
        title = self.langchain_wrapper.generate_completion(prompt=title_prompt)
        # remove surrounding quotes from title (if any)
        title = title.replace('"', "")
        return title

    def generate_cover(self, cover_template: str, title: str, topic: str, target_audience: str):
        doc = DocxTemplate(cover_template)

        img_data = self.langchain_wrapper.generate_photo("making money")
        with open("preview.png", "wb") as handler:
            handler.write(img_data)

        imagen = InlineImage(
            doc, "preview.png", width=Mm(120)
        )  # width is in millimetres
        context = {"title": title, "subtext": "NJ Publishing", "image": imagen}
        doc.render(context)
        doc.save("cover.pdf")

    def generate_ebook(self, topic: str, target_audience: str) -> str:
        print("starting generating the ebook")
        title = self.generate_title(topic=topic, target_audience=target_audience)

        template = {
            "cover_template": (
                "backend/app/templates/covers/gen.docx"
            ),
            "book_template": (
                "backend/app/templates/covers/office.docx"
            ),
        }

        self.generate_cover(template.get("cover_template"), title, topic, target_audience)

        return title


if __name__ == '__main__':
    ebook_generator = EbookGenerator()
    title = ebook_generator.generate_ebook(topic='making money',
                                           target_audience='mid age person looking for easy money')
    print("title: ", title)
