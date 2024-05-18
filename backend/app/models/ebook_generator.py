import uuid

from backend.app.models.langchain_wrapper import LangchainWrapper
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from docx2pdf import convert
import subprocess

class EbookGenerator:
    def __init__(self, temporary_id: str):
        self.langchain_wrapper = LangchainWrapper()
        self.cover_photo_location = (
            f"cover_photo-{temporary_id}.jpg"
        )
        self.cover_pdf_location = f"cover-{temporary_id}.pdf"
        self.cover_location = f"cover-{temporary_id}.docx"

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

    def generate_cover_photo(self,
                             title: str,
                             topic: str,
                             target_audience: str,
                             img_output: str):
        cover_prompt = (
            f'We have a ebook with the title {title}. It is about "{topic}".'
            f' Our reader is:  "{target_audience}". Write me a very brief and'
            " matter-of-fact description of a photo that would be on the"
            " cover of the book. Do not reference the cover or photo in your"
            ' answer. For example, if the title was "How to lose weight for'
            ' middle aged women", a reasonable response would be "a middle'
            ' age woman exercising"'
        )
        print("cover prompt", cover_prompt)
        photo_prompt = self.langchain_wrapper.generate_completion(prompt=cover_prompt)
        print("dalle prompt", photo_prompt)
        img_data = self.langchain_wrapper.generate_photo(photo_prompt=photo_prompt)
        with open(img_output, "wb") as f:
            f.write(img_data)

    def generate_cover(self, cover_template: str,
                       title: str,
                       topic: str,
                       target_audience: str,
                       output_file: str,
                       preview: bool):
        doc = DocxTemplate(cover_template)

        if preview:
            self.cover_photo_location = "app/templates/covers/preview_photo.png"
        else:
            self.generate_cover_photo(title=title, topic=topic, target_audience=target_audience,
                                      img_output=self.cover_photo_location)

        imagen = InlineImage(
            doc, self.cover_photo_location, width=Mm(120)
        )  # width is in millimetres
        context = {"title": title, "subtext": "Ebook Generator", "image": imagen}
        doc.render(context)
        doc.save(self.cover_location)
        # convert(self.cover_location, output_file)
        subprocess.call(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', self.cover_location, output_file])

    def generate_ebook(self, topic: str, target_audience: str) -> str:
        print("starting generating the ebook")
        title = self.generate_title(topic=topic, target_audience=target_audience)

        template = {
            "cover_template": (
                # "app/templates/covers/gen.docx"
                "gen.docx"
            ),
            "book_template": (
                "app/templates/covers/office.docx"
            ),
        }

        self.generate_cover(cover_template=template.get("cover_template"),
                            title=title,
                            topic=topic,
                            target_audience=target_audience,
                            output_file=self.cover_pdf_location,
                            preview=False)

        return title


if __name__ == '__main__':
    ebook_generator = EbookGenerator(temporary_id=str(uuid.uuid1()))
    title = ebook_generator.generate_ebook(topic='making money',
                                           target_audience='mid age person looking for easy money')
    print("title: ", title)
