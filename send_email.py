import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# CONFIG
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "akshay1988@gmail.com"
SENDER_PASSWORD = "xwqy xakj ktkw yeno"  # Use App Password, not real password!

# List of workstream owners
workstreams = {
    "Marketing": "aksdixit@cisco.com",
    "Engineering": "sayalee.agashe@gmail.com",
    ##"Sales": "person3@example.com",
}

def send_update_request():
    for stream, recipient in workstreams.items():
        subject = f"[Update Request] {stream} Workstream Status - {datetime.today().strftime('%b %d')}"
        body = f"""
Hi {stream} team,

Please provide your update in this format:

**Status:** (Green/Yellow/Red)  
**Progress:**  
**Risks:**  
**Mitigation:**

Thanks,  
Program Office
        """

        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"✅ Sent update request to {stream} ({recipient})")

if __name__ == "__main__":
    send_update_request()
