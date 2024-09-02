import os
import time
import random
from backend.app.models.ebook_generator import EbookGenerator
from backend.app.decorator.thread import threaded
from backend.app.aws.s3 import S3
from backend.app.resend.email_service import EmailService

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
            num_chapters=NUM_CHAPTERS,
            num_subsections=NUM_SUBSECTIONS,
            recipient_email=None,
            preview=False,
            sell=False,
            callback=None,
            id=None,
            add_to_shop=False
    ):
        if id == None:
            id = str(random.getrandbits(32)) + str(time.time())

        current_directory = os.getcwd()
        print("Current working directory:", current_directory)
        start_time = time.time()

        if preview:
            output_directory = "backend/app/preview/"
        else:
            output_directory = "backend/app/output/"

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

        if recipient_email:
            s3 = S3(S3_BUCKET, REGION)
            email_service = EmailService()

            # if permissions don't work, we want to fail early
            s3.try_permissions()

            print("Uploading to S3...")
            file_url = s3.upload_file(ebook.pdf_file, f"backend/app/output/final-{id}.pdf")
            print(
                f"Sending email to {recipient_email} with file url: {file_url}"
            )
            subject = email_service.generate_message(title=ebook.title,
                                                     topic=topic,
                                                     target_audience=target_audience,
                                                     id=id,
                                                     recipient_email=recipient_email,
                                                     file_url=file_url)

            email_service.send_email(subject=subject,
                                     title=ebook.title,
                                     recipient_email=recipient_email)

        if callback:
            s3 = S3(S3_BUCKET, REGION)

            # if permissions don't work, we want to fail early
            s3.try_permissions()
            # ses.try_permissions()

            print("Uploading to S3...")
            file_url = s3.upload_file(f"doc-{id}.pdf", ebook.pdf_file)

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
        topic="History of Maori Culture, and what happened to the Natives of New Zealand",
        target_audience="25, Maori Culture, New Zealand History",
        recipient_email="tweti0504@gmail.com"
    )
