# read_email.py
from __future__ import print_function
import os.path
import base64
from email import message_from_bytes
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If no valid credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save creds for next time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def read_update_emails(subject_filter="[Update Request]", days=7, senders=None, sender_email_to_exclude=None):
    """
    Reads emails matching the subject filter, from specified senders, excluding the sender_email_to_exclude,
    and only emails from the last `days` days.
    """
    service = get_gmail_service()

    # Build Gmail query
    q_parts = [f"subject:{subject_filter}", f"newer_than:{days}d"]
    if senders:
        sender_query = " OR ".join([f"from:{s}" for s in senders])
        q_parts.append(f"({sender_query})")
    if sender_email_to_exclude:
        q_parts.append(f"-from:{sender_email_to_exclude}")  # exclude your sent emails

    query = " ".join(q_parts)
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    updates = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = msg_data['payload']
        parts = payload.get('parts')
        data = None

        if parts:
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    data = base64.urlsafe_b64decode(part['body']['data']).decode()
                    break
        else:
            data = base64.urlsafe_b64decode(payload['body']['data']).decode()

        updates.append(data)

    return updates


if __name__ == "__main__":
    emails = read_update_emails()
    for i, email_body in enumerate(emails, 1):
        print(f"Email {i}:\n{email_body}\n{'-'*40}")
