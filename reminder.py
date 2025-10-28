from datetime import datetime, timedelta
from storage import get_all_updates
from send_email import send_update_request

# Optional: mapping of email -> workstream
WORKSTREAM_MAPPING = {
    "aksdixit@cisco.com": "Marketing",
    "sayalee.agashe@gmail.com": "Engineering",
    "person3@example.com": "Sales"
}

def get_delinquent_emails(workstreams_list, days=7):
    """Return emails for workstreams with no updates in the last `days` days."""
    all_updates = get_all_updates()

    cutoff = datetime.now() - timedelta(days=days)
    delinquent = []

    for email in workstreams_list:
        ws_name = WORKSTREAM_MAPPING.get(email)
        #print(f"\nLooking for ws_name: '{ws_name}'")
        ws_updates = [u for u in all_updates if u[0] == ws_name]
        #print(f"ws_updates: {ws_updates}")
        

        if not ws_updates:
            delinquent.append(email)
        else:
            latest_ts = max(datetime.fromisoformat(u[-1]) for u in ws_updates)
            if latest_ts < cutoff:
                delinquent.append(email)

    return delinquent




def send_reminder_emails(workstreams_list):
    """Find delinquent emails and send update requests."""
    delinquent_emails = get_delinquent_emails(workstreams_list)
    if not delinquent_emails:
        print(f"[{datetime.now()}] All workstreams have updates. No reminders sent.")
        return

    print(f"[{datetime.now()}] Sending reminders to: {delinquent_emails}")
    send_update_request(recipients=delinquent_emails)
