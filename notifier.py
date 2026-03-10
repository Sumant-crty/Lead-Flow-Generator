import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_report(recipient_email, report_path):
    # Email credentials (Use Environment Variables or App Passwords for security)
    sender_email = "your_email@gmail.com" 
    password = "your_app_password" 

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = "📊 Periodic Lead Research Report"

    body = "Please find the latest lead research report attached. All data has been verified and cleaned."
    message.attach(MIMEText(body, 'plain'))

    # Attachment logic
    filename = os.path.basename(report_path)
    with open(report_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        message.attach(part)

    # Connect to Server (Gmail example)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)
        server.quit()
        print(f"📧 Report successfully sent to {recipient_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")