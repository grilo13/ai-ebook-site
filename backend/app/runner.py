import os
import time
import random
from backend.app.models.ebook_generator import EbookGenerator
from backend.app.decorator.thread import threaded
from backend.app.aws.s3 import S3

S3_BUCKET = "ai-new"
SENDER = "nulllabsllc@gmail.com"
REGION = "eu-north-1"
EBOOK_READY_EMAIL_SUBJECT = "Your AI-generated ebook is ready!"

"""
Main class
"""

NUM_CHAPTERS = 6
NUM_SUBSECTIONS = 4


class Runner:
    # @retry(max_retries=3)
    @threaded
    def create_ebook(
            self,
            topic,
            target_audience,
            recipient_email,
            preview=False,
            sell=False,
            callback=None,
            id=None,
            add_to_shop=False,
            num_chapters=NUM_CHAPTERS,
            num_subsections=NUM_SUBSECTIONS,
    ):
        if id == None:
            id = str(random.getrandbits(32)) + str(time.time())

        current_directory = os.getcwd()
        print("Current working directory:", current_directory)
        start_time = time.time()

        if preview:
            output_directory = "../preview/"
        else:
            output_directory = "../output/"

        eg = EbookGenerator(
            id=id,
            output_directory=output_directory
        )

        ebook = eg.generate_ebook(
            topic=topic,
            target_audience=target_audience,
            id=id,
            num_chapters=num_chapters,
            num_subsections=num_subsections,
            preview=preview
        )

        if callback:
            s3 = S3(S3_BUCKET, REGION)
            # ses = SES(SENDER, REGION)

            # if permissions don't work, we want to fail early
            s3.try_permissions()
            # ses.try_permissions()

            print("Uploading to S3...")
            # file_url = s3.upload_file(ebook.pdf_file, f"{id}.pdf")
            file_url = s3.upload_file(f"doc-{id}.docx", ebook.docx_file)

            callback(id, "completed", file_url)

        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_minutes, elapsed_seconds = divmod(elapsed_time, 60)
        print(
            f"Elapsed time: {int(elapsed_minutes)} minutes and"
            f" {elapsed_seconds:.2f} seconds"
        )

        return {
            "message": (
                "Successfully created ebook!"
                f"Elapsed time: {int(elapsed_minutes)} minutes and"
                f" {elapsed_seconds:.2f} seconds"
            )
        }


if __name__ == "__main__":
    runner = Runner()
    runner.create_ebook(
        "History of Maori Culture, and what happened to the Natives of New Zealand",
        "25, Maori Culture, New Zealand History",
        "tweti0504@gmail.com"
    )
