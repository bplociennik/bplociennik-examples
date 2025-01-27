import os
import smtplib
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from jinja2 import Environment, FileSystemLoader


@dataclass
class Attachment:
    path: str
    content_name: str


def send_message(
    email_from: str,
    email_subject: str,
    email_to: str,
    html_template: str,
    txt_template: str,
    attachments: list[Attachment],
) -> None:

    msg = MIMEMultipart("alternative")
    msg["From"] = email_from
    msg["Subject"] = email_subject
    msg["To"] = email_to

    # Use Jinja2 to render templates
    env = Environment(loader=FileSystemLoader("templates"))
    html_template = env.get_template(html_template)
    txt_template = env.get_template(txt_template)
    
    # Pass context to templates
    rendered_html_template = html_template.render({
        "fire_content_id": "fire",
        "mountains_content_id": "mountains",
    })
    rendered_txt_template = txt_template.render()

    msg.attach(MIMEText(rendered_html_template, "html"))
    msg.attach(MIMEText(rendered_txt_template, "plain"))

    # Attach images into email
    for attachment in attachments:
        path = os.path.abspath(attachment.path)
        with open(path, "rb") as file:
            content_file = MIMEImage(file.read())
            content_file.add_header(
                "Content-ID",
                f"<{attachment.content_name}>",
            )
            msg.attach(content_file)

    server = smtplib.SMTP(host="mailpit", port=1025)
    server.send_message(msg=msg)


if __name__ == "__main__":
    print("Sending message....")

    jpg_attachment = Attachment(
        path="images/fire.jpg",
        content_name="fire",
    )
    webp_attachment = Attachment(
        path="images/mountains.webp",
        content_name="mountains",
    )

    send_message(
        email_from="from@example.com",
        email_subject="Welcome to the jungle",
        email_to="to@example.pl",
        html_template="welcome.html",
        txt_template= "welcome.txt",
        attachments=[jpg_attachment, webp_attachment],
    )

    print("Message sent! Open your local mailbox http://localhost:8025/")
