import sqlite3
from datetime import datetime
import json
import os

DB_PATH = "program_updates.db"

def init_db():
    """Create the table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workstream TEXT,
            status TEXT,
            progress TEXT,
            risks TEXT,
            mitigation TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_update(workstream, parsed_json):
    """Insert one parsed update into the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO updates (workstream, status, progress, risks, mitigation, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        workstream,
        parsed_json.get("Status", "N/A"),
        parsed_json.get("Progress", "N/A"),
        parsed_json.get("Risks", "N/A"),
        parsed_json.get("Mitigation", "N/A"),
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()
    #print("✅ Test row added.")

def get_all_updates():
    """Fetch all stored updates."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT workstream, status, progress, risks, mitigation, timestamp FROM updates")
    rows = c.fetchall()
    conn.close()
    return rows
