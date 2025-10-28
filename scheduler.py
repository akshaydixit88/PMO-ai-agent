# scheduler_simple.py
"""
Minimal, safe scheduler that calls only the functions you provided in agent.py.

Note:
- This uses the 'schedule' package (simple, local scheduler).
- Times are local machine time. If you want PT, run this on a machine set to PT or use cron/Cloud scheduler.
- Polling job uses the same index-based mapping approach your agent previously used.
"""

import time
import json
import schedule
from datetime import datetime

# Import the exact functions you already have
from send_email import send_update_request            # your send_email.py
from read_email import read_update_emails            # your read_email.py
from parse_email import parse_update                 # your parse_email.py
from storage import init_db, save_update, get_all_updates
from generate_summary import generate_exec_summary
from generate_dashboard_from_exec import generate_dashboard_from_exec
from config import RECIPIENTS, SENDER_EMAIL
from reminder import send_reminder_emails

# Workstream mapping (same approach used in agent.py)
WORKSTREAMS = ["Marketing", "Engineering", "Sales"]  # keep consistent with your mapping strategy

# --- Jobs ------------------------------------------------------------------

def job_send_monday_requests():
    print(f"[{datetime.now()}] Running Monday send job...")
    try:
        # call your existing send function
        send_update_request()   # if your function accepts args, adjust accordingly
        print("Sent weekly update requests.")
    except Exception as e:
        print("Error in sending weekly requests:", e)

def job_send_wed_reminders():
    send_reminder_emails(RECIPIENTS)

def job_poll_and_store():
    print(f"[{datetime.now()}] Polling for email updates...")
    try:
        updates = read_update_emails(
            subject_filter="[Update Request]",
            days=7,
            senders=RECIPIENTS,
            sender_email_to_exclude=SENDER_EMAIL
        )
        if not updates:
            print("No updates found on poll.")
            return

        init_db()
        # replicate earlier index mapping approach
        for i, email_body in enumerate(updates):
            try:
                parsed = parse_update(email_body)
                # parse_update in your setup returned JSON-string — try to load, else handle dict/string
                try:
                    parsed_json = json.loads(parsed) if isinstance(parsed, str) else parsed
                except Exception:
                    # fallback: put the raw text into Progress
                    parsed_json = {"Status": "N/A", "Progress": parsed if isinstance(parsed, str) else str(parsed), "Risks": "", "Mitigation": ""}
            except Exception as e:
                print(f"Error parsing email #{i}: {e}")
                parsed_json = {"Status": "N/A", "Progress": "", "Risks": "", "Mitigation": ""}

            # map index -> workstream (same brittle mapping as before)
            workstream = WORKSTREAMS[i] if i < len(WORKSTREAMS) else f"Workstream_{i}"
            try:
                save_update(workstream, parsed_json)
                print(f"Saved update for {workstream}")
            except Exception as e:
                print(f"Failed to save update for {workstream}: {e}")

    except Exception as e:
        print("Polling failed:", e)

def job_generate_and_save_summary():
    print(f"[{datetime.now()}] Generating exec summary and slide...")
    try:
        summary_text = generate_exec_summary(api_key=None)  # your function expects OPENAI_API_KEY internally or pass if needed
        # generate_dashboard_from_exec returns output filename (per your implementation)
        output_file = generate_dashboard_from_exec(summary_text)
        print("Generated dashboard:", output_file)
    except Exception as e:
        print("Error generating/saving summary:", e)

# --- Scheduler setup ------------------------------------------------------

def start():
    # schedule jobs (local machine time)
    schedule.every().sunday.at("16:13").do(job_send_monday_requests)
    schedule.every().sunday.at("17:23").do(job_send_wed_reminders)
    schedule.every(10).minutes.do(job_poll_and_store)
    schedule.every().wednesday.at("17:00").do(job_generate_and_save_summary)

    print("Scheduler started. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start()
