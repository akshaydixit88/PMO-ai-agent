# PMO AI Agent 🧠

An AI-powered Program Management Office (PMO) assistant that automates status updates, parses responses, and generates executive summaries — this is an MVP built over a weekend using Python and LLMs.

🎥 Demo: 


## 🚀 Overview

This project automates routine PMO tasks such as collecting status updates from workstream owners, structuring them into a database, and generating executive reports — all powered by an AI agent running on a schedule.

**Key Features:**
- Sends automated email requests for program updates. Reminders to delinquients 
- Reads and parses Gmail responses using LLM → structured JSON (status, risks, next steps)  
- Stores parsed data into a local database  
- Generates an executive summary report on a set schedule  

---

## 🧰 Tech Stack

- **Python**
- **OpenAI API** – for text parsing and summarization  
- **Google Gmail API** – for reading and sending emails  
- **Schedule / Cron** – for automation  
- **SQLite / JSON** – for data storage  
- **dotenv** – for managing environment variables  

---

## ⚙️ Setup Instructions

```bash
1️⃣ Clone the repo
git clone https://github.com/akshaydixit88/PMO-ai-agent.git
cd PMO-ai-agent

2️⃣ Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Set up your .env file
cp .env.example .env
Fill in your API keys and credentials:
OPENAI_API_KEY=your_api_key_here
EMAIL_ADDRESS=your_email_here
EMAIL_PASSWORD=your_password_here

5️⃣ Set up Gmail API credentials
This project currently uses the Gmail API for reading and sending program update emails.
Follow these steps:
Go to the Google Cloud Console.
Create a new project (or use an existing one).
Enable the Gmail API for your project.
Under APIs & Services → Credentials, create OAuth 2.0 Client IDs.
Download the file named credentials.json and place it in your project folder.
The first time you run the script, you’ll be asked to log in with your Gmail account — this will create a token.json file automatically.
credentials.json = the Google Cloud key to access Gmail API
token.json = your authorization token to send and read emails
You’ll now have both files in your folder:
credentials.json
token.json

6️⃣ Run the agent
python scheduler.py

🧩 How It Works
The agent runs on a set schedule and sends update requests to program owners via Gmail.
Incoming responses are automatically fetched using the Gmail API.
The LLM parses the content into structured JSON:
{
  "workstream": "Marketing",
  "status": "On track",
  "progress":"Things are good",
  "risks": "Dependency on vendor X"
}
These records are saved into a local database.
On a defined date, the agent generates an executive summary combining all updates.

```
---

**## 🔮 Roadmap**
Adding Microsoft/Outlook integration
Web dashboard for adding new programs and workstream owners 


**## 📜 License**
MIT License
