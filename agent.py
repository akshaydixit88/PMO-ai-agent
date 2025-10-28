from openai import OpenAI
from email_tools import send_update_request_emails
from send_email import send_update_request
from config import OPENAI_API_KEY
from read_email import read_update_emails
from config import RECIPIENTS, SENDER_EMAIL
from parse_email import parse_update 
from storage import init_db, save_update
from storage import get_all_updates
import json
from generate_summary import generate_exec_summary
from generate_summary import create_summary_slide
from generate_dashboard_from_exec import generate_dashboard_from_exec
from datetime import datetime, timedelta
from storage import get_all_updates


client = OpenAI(api_key=OPENAI_API_KEY)

def main():
    print("Initializing Program Dashboard Agent...\n")

    # Step 1: Send update request emails
    #result = send_update_request()
    #print(result)

    # Step 2: (Next) Read responses from inbox
    updates = read_update_emails(
        subject_filter="[Update Request]",
        days=7,
        senders=RECIPIENTS,
        sender_email_to_exclude=SENDER_EMAIL
    )
    #print("\nFetched Updates:")
    #for i, email_body in enumerate(updates, 1):
    #    print(f"Email {i}:\n{email_body}\n{'-'*40}")

    # Step 3: (Next) Parse and store updates
    structured_updates = []
    workstreams = {
        "Marketing": "abc@xyz.com",
        "Engineering": "pqr@gmail.com",
        "Sales": "person3@example.com",
    }
    for email_body in updates:
        parsed = parse_update(email_body)
        structured_updates.append(parsed)
        print(parsed)
    
    init_db()
    for i, email_body in enumerate(updates):
        parsed = parse_update(email_body)
        parsed_json = json.loads(parsed)
        workstream = list(workstreams.keys())[i]  # or however you map senders → workstreams
        save_update(workstream, parsed_json)

   
    # Step 4: (Next) Generate executive summary / slides
    summary_text = generate_exec_summary(api_key=OPENAI_API_KEY)
    #print(summary_text)
    #create_summary_slide(summary_text, "Weekly_Exec_Summary.pptx")
    generate_dashboard_from_exec(summary_text)



if __name__ == "__main__":
    main()