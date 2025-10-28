from openai import OpenAI
from config import OPENAI_API_KEY
import json

client = OpenAI(api_key=OPENAI_API_KEY)

def parse_update(email_text):
    """
    Converts raw email text into structured JSON with keys:
    Status, Progress, Risks, Mitigation
    """
    prompt = f"""
Extract structured fields from this email. Output JSON only with keys:
Status, Progress, Risks, Mitigation

Rules:
- Status must be one of "Green", "Yellow", or "Red". 
- Use the email text to decide the Status.
- Progress, Risks, and Mitigation can be full sentences.
- If a field is missing, output "N/A".


Email:
{email_text}
"""
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}]
    )
    parsed_json = response.choices[0].message.content
    return parsed_json
