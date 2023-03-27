import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from jinja2 import Template


SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "admin@bloglite.com"
SENDER_PASSWORD = ""

def send_email(to_address, subject, message, msgImage):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, 'html'))
    msg.attach(msgImage)

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

    return True


def send_reminder_email(to_email, username, days_count):
    with open("static/img/logo.png", 'rb') as img:
        msgImage = MIMEImage(img.read())
        msgImage.add_header('Content-ID', '<logo>')

    with open("templates/reminder.html") as file:
        template = Template(file.read())
        message =  template.render(username = username, days_count = days_count)

    send_email(to_email, "DAILY REMINDER", message, msgImage)

    return True

def send_monthly_report(to_email, username, month, data):
    with open("static/img/logo.png", 'rb') as img:
        msgImage = MIMEImage(img.read())
        msgImage.add_header('Content-ID', '<logo>')

    with open("templates/report.html") as file:
        template = Template(file.read())
        message =  template.render(username = username, month = month, data=data)

    send_email(to_email, "Monthly Engagement Report - {}".format(month), message, msgImage)

    return True