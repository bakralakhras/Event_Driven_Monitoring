from fastapi import FastAPI, Request
from pydantic import BaseModel
import logging
import cohere
import os
import subprocess
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
logging.info(f"🔍 SLACK_WEBHOOK_URL: {SLACK_WEBHOOK_URL if SLACK_WEBHOOK_URL else '❌ MISSING'}")

cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    logging.error("❌ COHERE_API_KEY is missing!")

client = cohere.Client(cohere_api_key)

app = FastAPI()

class Incident(BaseModel):
    labels: dict
    annotations: dict

def generate_ai_response(description: str):
    try:
        response = client.generate(
            model="command",
            prompt=f"Incident detected: {description}. Provide troubleshooting steps."
        )
        ai_suggestion = response.generations[0].text if response.generations else "No AI response."
        logging.info(f"AI Suggestion: {ai_suggestion}")
        return ai_suggestion
    except Exception as e:
        logging.error(f"Cohere API Error: {e}")
        return "Error: Failed to generate AI response."

def should_remediate(alert_description: str, ai_suggestion: str):
    """Determine if auto-remediation should be triggered based on alert and AI suggestion"""
    # CPU-related issues
    if "cpu" in alert_description.lower() or "cpu" in ai_suggestion.lower():
        return True
    
    # Service-related issues that need restart
    if any(phrase in ai_suggestion.lower() for phrase in ["restart service", "restart the service", "service restart"]):
        return True
        
    return False

def auto_remediate(alert_description: str, ai_suggestion: str):
    logging.info(f"Auto-remediation triggered for: {alert_description}")

    if "cpu" in alert_description.lower() or "cpu" in ai_suggestion.lower():
        try:
            subprocess.run(["docker", "exec", "demo-vm", "pkill", "-f", "yes"], check=True)
            logging.info("Successfully killed high CPU processes.")
            return "Killed high CPU processes"
        except Exception as e:
            logging.error(f"Failed to kill high CPU processes: {e}")
            return f"Failed: {str(e)}"

    elif any(phrase in ai_suggestion.lower() for phrase in ["restart service", "restart the service", "service restart"]):
        try:
            subprocess.run(["docker", "exec", "demo-vm", "service", "nginx", "restart"], check=True)
            logging.info("Successfully restarted the service.")
            return "Restarted nginx service"
        except Exception as e:
            logging.error(f"Failed to restart service: {e}")
            return f"Failed: {str(e)}"
    
    return "No remediation actions performed"

def send_to_slack(incident: Incident, ai_suggestion: str, remediation_result: str = None):
    if not SLACK_WEBHOOK_URL:
        logging.error("SLACK_WEBHOOK_URL is missing!")
        return

    logging.info(f"Sending alert to Slack Webhook: {SLACK_WEBHOOK_URL}")

    message = {
        "text": f":rotating_light: *Incident Alert!*\n"
                f"*Alert Name:* {incident.labels.get('alertname', 'Unknown')}\n"
                f"*Severity:* {incident.labels.get('severity', 'Unknown')}\n"
                f"*Description:* {incident.annotations.get('description', 'No description provided.')}\n\n"
                f"*AI Suggestion:*\n{ai_suggestion}"
    }

    if remediation_result:
        message["text"] += f"\n\n*Auto-remediation:*\n{remediation_result}"

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        logging.info(f"Slack Response Code: {response.status_code}")
        logging.info(f"Slack Response Body: {response.text}")

        if response.status_code == 200:
            logging.info("✅ Incident successfully sent to Slack.")
        else:
            logging.error(f"Failed to send incident to Slack: {response.text}")

    except Exception as e:
        logging.error(f"Slack Webhook Error: {e}")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    logging.info(f"Incoming Request: {request.method} {request.url} \nHeaders: {dict(request.headers)} \nBody: {body.decode()}")
    response = await call_next(request)
    return response

@app.post("/incident")
async def receive_incident(request: Request):
    data = await request.json()
    logging.info(f"RAW DATA RECEIVED: {data}")

    alerts = data.get("alerts", [])
    logging.info(f"EXTRACTED ALERTS: {alerts}")

    processed_alerts = []

    for alert in alerts:
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})

        logging.info(f"EXTRACTED LABELS: {labels}")
        logging.info(f"EXTRACTED ANNOTATIONS: {annotations}")

        incident = Incident(labels=labels, annotations=annotations)
        logging.info(f"PROCESSED INCIDENT: {incident}")

        description = incident.annotations.get("description", "No description provided.")
        
        # Generate AI suggestion
        ai_suggestion = generate_ai_response(description)
        
        # Check if auto-remediation is needed
        remediation_result = None
        if should_remediate(description, ai_suggestion):
            logging.info(f"Auto-remediation needed for: {description}")
            remediation_result = auto_remediate(description, ai_suggestion)

        
        # Send to Slack with remediation results if available
        send_to_slack(incident, ai_suggestion, remediation_result)

        processed_alerts.append({
            "alert_name": incident.labels.get("alertname", "Unknown"),
            "severity": incident.labels.get("severity", "Unknown"),
            "description": description,
            "ai_suggestion": ai_suggestion,
            "remediation_result": remediation_result
        })

    return {"message": "Alert received and processed", "alerts": processed_alerts}