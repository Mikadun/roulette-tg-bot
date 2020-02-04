import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_mail(host_mail, host_password, subject, receiver, content):
    message = MIMEMultipart()
    message['From'] = host_mail
    message['To'] = receiver
    message['Subject'] = subject
    message.attach(MIMEText(content, 'plain'))
    message = message.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(host_mail, host_password)
    server.sendmail(host_mail, receiver, message)
    server.quit()

def verification_mail(receiver, code):
    host = os.getenv('EMAIL_HOST')
    password = os.getenv('EMAIL_PASSWORD')
    content = 'Your authentication code is {code}'.format(code = code)
    subject = 'Authentication code for roulette bot'
    send_mail(host, password, subject, receiver, content)

if __name__ == '__main__':
    verification_mail('gribak98@gmail.com', 0)
