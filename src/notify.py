import smtplib
from email.mime.text import MIMEText


class Notifier:

    def __init__(self, email_from, email_to, smtp_server, smtp_port, password):

        self.email_from = email_from
        self.email_to = email_to
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.password = password

    def send(self, subject, message):

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = self.email_from
        msg["To"] = self.email_to

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.email_from, self.password)
            server.send_message(msg)