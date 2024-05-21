import json
import os
import uuid

from backend.app.models.langchain_wrapper import LangchainWrapper
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from docx2pdf import convert
from docx import Document
import subprocess
import pypandoc
from backend.app.models.ebook import Ebook


class EbookGenerator:
    def __init__(self, id: str, output_directory: str):
        self.langchain_wrapper = LangchainWrapper()
        self.output_directory = output_directory
        self.cover_photo_location = (
            f"cover_photo-{id}.jpg"
        )
        self.cover_pdf_location = f"cover-{id}.pdf"
        self.cover_location = f"cover-{id}.docx"

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
        try:
            subprocess.call(
                ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', self.cover_location, output_file])
        except Exception as err:
            print("something went wrong writing the file", err.__str__())

        try:
            pypandoc.convert_file(self.cover_location, 'pdf', outputfile=output_file)
        except Exception as err:
            print("error 2", err.__str__())

    def generate_outline(
            self,
            topic,
            target_audience,
            title,
            num_chapters,
            num_subsections,
    ):
        outline_prompt = (
            f'We are writing an eBook called "{title}". It is about'
            f' "{topic}". Our reader is:  "{target_audience}".  Create'
            " a compehensive outline for our ebook, which will have"
            f" {num_chapters} chapter(s). Each chapter should have exactly"
            f" {num_subsections} subsection(s) Output Format for prompt:"
            " python dict with key: chapter title, value: a single list/array"
            " containing subsection titles within the chapter (the subtopics"
            " should be inside the list). The chapter titles should be"
            ' prepended with the chapter number, like this: "Chapter 5:'
            ' [chapter title]". The subsection titles should be prepended'
            ' with the {chapter number.subtitle number}, like this: "5.4:'
            ' [subsection title]". '
        )
        outline_json = self.langchain_wrapper.generate_completion(prompt=outline_prompt)
        print("outline json", outline_json)
        outline_json = outline_json[
                       outline_json.find("{"): outline_json.rfind("}") + 1
                       ]
        print("outline json", outline_json)
        outline = json.loads(outline_json)
        """if not self.verify_outline(outline, num_chapters, num_subsections):
            raise Exception("Outline not well formed!")"""

        return outline

    def generate_chapter_content(self, topic: str,
                                 target_audience: str,
                                 title: str,
                                 idx: int,
                                 chapter: str,
                                 subtopic: str):
        num_words_str = "500 to 700"
        content_prompt = (
            f'We are writing an eBook called "{title}". Overall, it is about'
            f' "{topic}". Our reader is:  "{target_audience}". We are'
            f" currently writing the #{idx + 1} section for the chapter:"
            f' "{chapter}". Using at least {num_words_str} words, write the'
            " full contents of the section regarding this subtopic:"
            f' "{subtopic}". The output should be as helpful to the reader as'
            " possible. Include quantitative facts and statistics, with"
            " references. Go as in depth as necessary. You can split this"
            " into multiple paragraphs if you see fit. The output should also"
            ' be in cohesive paragraph form. Do not include any "[Insert'
            ' ___]" parts that will require manual editing in the book later.'
            " If find yourself needing to put 'insert [blank]' anywhere, do"
            " not do it (this is very important). If you do not know"
            " something, do not include it in the output. Exclude any"
            " auxiliary information like  the word count, as the entire"
            " output will go directly into the ebook for readers, without any"
            " human processing. Remember the {num_words_str} word minimum,"
            " please adhere to it."
        )
        content = self.langchain_wrapper.generate_completion(prompt=content_prompt)
        return content

    def generate_docx(self,
                      topic: str,
                      target_audience: str,
                      title: str,
                      outline: dict,
                      docx_file: str,
                      book_template: str,
                      preview: bool,
                      actionable_steps: bool = False):
        print("generating docx")
        document = Document(book_template)
        document.add_page_break()
        document.add_heading("Table of Contents")
        for chapter, subtopics in outline.items():
            print("chapter", chapter)
            print("subtopics", subtopics)
            document.add_heading(chapter, level=2)
            for idx, subtopic in enumerate(subtopics):
                print("idx", idx)
                print("subtopic", subtopic)
                document.add_heading("\t" + subtopic, level=3)

        document.add_page_break()

        chapter_num = 1
        for chapter, subtopics in outline.items():
            document.add_heading(chapter, level=1)
            subtopics_content = []

            # Generate each subtopic content
            for idx, subtopic in enumerate(subtopics):
                # Stop writing the ebook after four subsections if preview
                print("preview and idx", preview, idx)
                if preview and idx >= 2:
                    break
                document.add_heading(subtopic, level=2)
                content = self.generate_chapter_content(
                    topic=topic, target_audience=target_audience, title=title,
                    idx=idx, chapter=chapter, subtopic=subtopic
                )
                document.add_paragraph(content)

            if preview:
                document.add_heading(
                    "Preview Completed - Purchase Full Book To Read More!"
                )
                break

            if chapter_num < len(outline.items()):
                document.add_page_break()
            chapter_num += 1

        document.add_page_break()

        document.save(docx_file)

    def generate_ebook(self,
                       topic: str,
                       target_audience: str,
                       id: str,
                       num_chapters: int = 6,
                       num_subsections: int = 4,
                       preview: bool = True) -> Ebook:
        print("starting generating the ebook")

        docx_file = f"backend/app/docs/docs-{id}.docx"

        title = self.generate_title(topic=topic, target_audience=target_audience)

        print("directory ", os.getcwd())

        template = {
            "cover_template": (
                "backend/app/templates/covers/gen.docx"
            ),
            "book_template": (
                "backend/app/templates/content/theme.docx"
            ),
        }

        """
        self.generate_cover(cover_template=template.get("cover_template"),
                            title=title,
                            topic=topic,
                            target_audience=target_audience,
                            output_file=self.cover_pdf_location,
                            preview=False)"""

        outline = self.generate_outline(
            topic,
            target_audience,
            title,
            num_chapters,
            num_subsections,
        )

        self.generate_docx(topic=topic,
                           target_audience=target_audience,
                           title=title,
                           outline=outline,
                           docx_file=docx_file,
                           book_template=template.get("book_template"),
                           preview=preview)

        return Ebook(title=title,
                     topic=topic,
                     target_audience=target_audience,
                     docx_file=docx_file)


if __name__ == '__main__':
    ebook_generator = EbookGenerator(id=str(uuid.uuid1()),
                                     output_directory="../preview/")
    ebook = ebook_generator.generate_ebook(topic='how to lose weight',
                                           target_audience='mid age moms',
                                           id=str(uuid.uuid1()),
                                           preview=True)
    print("ebook title: ", ebook.title)
    print("ebook topic: ", ebook.topic)

