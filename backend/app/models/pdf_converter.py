from typing import Optional
import subprocess
import re


# github gist: https://gist.github.com/MichalZalecki/92fd007699004ae7d806274d3a0d5476
# post: https://michalzalecki.com/converting-docx-to-pdf-using-python/
class PDFConverter:
    def __init__(self):
        self.default_exec = 'libreoffice'

    def convert_to(self, docx: str, folder: Optional[str] = '', timeout=None):
        args = [self.default_exec, '--headless', '--convert-to', 'pdf', '--outdir', folder, docx]

        process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        filename = re.search('-> (.*?) using filter', process.stdout.decode())

        if filename is None:
            print("error - ", process.stdout.decode())
            raise LibreOfficeError(process.stdout.decode())
        else:
            return filename.group(1)

    @staticmethod
    def libreoffice_exec():
        # TODO: Provide support for more platforms
        return 'libreoffice'


class LibreOfficeError(Exception):
    def __init__(self, output):
        self.output = output


if __name__ == '__main__':
    converter = PDFConverter()
    converter.convert_to(docx='../docs/docs-30123372231716333231.1260004.docx')
