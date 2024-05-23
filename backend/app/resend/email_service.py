import resend

from backend.app.core.config import settings

resend.api_key = settings.RESEND_API_KEY


class EmailService:
    def __init__(self):
        self.email_sender = settings.EMAIL_SENDER

    def send_email(self, subject: str, title: str, recipient_email: str):
        params = {
            "from": self.email_sender,
            "to": [recipient_email],
            "subject": f"Your AI-Generated eBook '{title}' is Ready for Download",
            "html": subject
        }

        email = resend.Emails.send(params)
        print(email)

        return 200

    @staticmethod
    def generate_message(title: str, topic: str, target_audience: str, id: id, recipient_email: str, file_url: str):
        message = f"""
        <p>Hi,</p>
        <p>We are excited to inform you that your AI-generated eBook is now ready for download. Here are the details:</p>
        <p><strong>Title:</strong> {title}</p>
        <p><strong>Topic:</strong> {topic}</p>
        <p><strong>Reader:</strong> {target_audience}</p>
        <p><strong>Id:</strong> {id}</p>
        <p><strong>Email:</strong> {recipient_email}</p>
        <p><a href="{file_url}" class="button">View your full E-Book here</a></p>
        """

        return message
