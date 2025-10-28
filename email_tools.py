from config import RECIPIENTS, SENDER_EMAIL

def send_update_request_emails():
    subject = "Weekly Program Update Request"
    body = (
        "Hi team,\n\n"
        "Please share your weekly update in the format below:\n\n"
        "Status (Green/Amber/Red):\n"
        "Progress Summary:\n"
        "Risks:\n"
        "Mitigation Plan:\n\n"
        "Thanks!"
    )

    for recipient in RECIPIENTS:
        print(f"Simulating email send → To: {recipient}")
        print(f"Subject: {subject}")
        print(f"Body:\n{body}")
        print("-" * 40)

    return f"Simulated sending {len(RECIPIENTS)} emails from {SENDER_EMAIL}"