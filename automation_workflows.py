import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict, Any
from cannabis_classifier import ClassificationResult, PriorityLevel


class AutomationWorkflows:
    def __init__(self):
        self.slack_webhook_url = "https://hooks.slack.com/services/YOUR_WEBHOOK_URL"
        self.email_config = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "cannabis-alerts@yourcompany.com",
            "sender_password": "your_app_password"
        }
        self.log_file = "automation_log.json"

    def send_slack_alert(self, result: ClassificationResult) -> Dict[str, Any]:
        """Send immediate Slack alert for HIGH priority documents."""
        message = {
            "text": "🚨 HIGH PRIORITY CANNABIS DOCUMENT DETECTED",
            "attachments": [
                {
                    "color": "#ff0000",
                    "fields": [
                        {
                            "title": "Document",
                            "value": result.document_name,
                            "short": True
                        },
                        {
                            "title": "Score",
                            "value": str(result.score),
                            "short": True
                        },
                        {
                            "title": "Reasoning",
                            "value": result.reasoning,
                            "short": False
                        },
                        {
                            "title": "Key Phrases",
                            "value": ", ".join(result.key_phrases[:5]),
                            "short": False
                        },
                        {
                            "title": "Recommended Action",
                            "value": "IMMEDIATE FOLLOW-UP REQUIRED",
                            "short": False
                        }
                    ],
                    "footer": f"Processed at {result.processed_at.strftime('%Y-%m-%d %H:%M:%S')}"
                }
            ]
        }
        
        # Mock Slack API call
        print(f"🔴 SLACK ALERT SENT: {result.document_name}")
        print(json.dumps(message, indent=2))
        
        return {
            "status": "success",
            "platform": "slack",
            "message": message,
            "timestamp": datetime.now().isoformat()
        }

    def send_weekly_digest(self, results: List[ClassificationResult]) -> Dict[str, Any]:
        """Send weekly digest email for MEDIUM priority documents."""
        medium_priority_docs = [r for r in results if r.classification == PriorityLevel.MEDIUM_PRIORITY]
        
        if not medium_priority_docs:
            return {"status": "no_medium_priority_docs", "message": "No medium priority documents to report"}
        
        # Create email content
        subject = f"Weekly Cannabis Document Digest - {datetime.now().strftime('%Y-%m-%d')}"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 15px; border-radius: 5px; }}
                .document {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
                .score {{ font-weight: bold; color: #ff6600; }}
                .key-phrases {{ color: #666; font-style: italic; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🌿 Weekly Cannabis Document Digest</h2>
                <p>Date: {datetime.now().strftime('%Y-%m-%d')}</p>
                <p>Total Medium Priority Documents: {len(medium_priority_docs)}</p>
            </div>
        """
        
        for doc in medium_priority_docs:
            html_content += f"""
            <div class="document">
                <h3>{doc.document_name}</h3>
                <p><span class="score">Score: {doc.score}</span></p>
                <p><strong>Reasoning:</strong> {doc.reasoning}</p>
                <p class="key-phrases"><strong>Key Phrases:</strong> {', '.join(doc.key_phrases)}</p>
                <p><strong>Recommended Action:</strong> Monitor and plan</p>
            </div>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        # Mock email sending
        print(f"📧 WEEKLY DIGEST EMAIL SENT: {len(medium_priority_docs)} medium priority documents")
        print(f"Subject: {subject}")
        print("Email content would be sent to stakeholders")
        
        return {
            "status": "success",
            "platform": "email",
            "subject": subject,
            "recipients": ["stakeholders@yourcompany.com"],
            "document_count": len(medium_priority_docs),
            "timestamp": datetime.now().isoformat()
        }

    def log_low_priority(self, results: List[ClassificationResult]) -> Dict[str, Any]:
        """Log LOW priority documents to JSON file."""
        low_priority_docs = [r for r in results if r.classification == PriorityLevel.LOW_PRIORITY]
        
        if not low_priority_docs:
            return {"status": "no_low_priority_docs", "message": "No low priority documents to log"}
        
        # Prepare log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "low_priority_log",
            "document_count": len(low_priority_docs),
            "documents": []
        }
        
        for doc in low_priority_docs:
            log_entry["documents"].append({
                "document_name": doc.document_name,
                "score": doc.score,
                "reasoning": doc.reasoning,
                "key_phrases": doc.key_phrases,
                "processed_at": doc.processed_at.isoformat()
            })
        
        # Append to log file
        try:
            with open(self.log_file, 'r') as f:
                existing_logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_logs = []
        
        existing_logs.append(log_entry)
        
        with open(self.log_file, 'w') as f:
            json.dump(existing_logs, f, indent=2)
        
        print(f"📝 LOW PRIORITY LOGGED: {len(low_priority_docs)} documents added to {self.log_file}")
        
        return {
            "status": "success",
            "action": "logged",
            "log_file": self.log_file,
            "document_count": len(low_priority_docs),
            "timestamp": datetime.now().isoformat()
        }

    def process_automation_workflows(self, results: List[ClassificationResult]) -> Dict[str, Any]:
        """Process all automation workflows based on document classifications."""
        automation_results = {
            "timestamp": datetime.now().isoformat(),
            "total_documents": len(results),
            "workflows_executed": {}
        }
        
        # Process HIGH priority documents (immediate Slack alerts)
        high_priority_docs = [r for r in results if r.classification == PriorityLevel.HIGH_PRIORITY]
        if high_priority_docs:
            automation_results["workflows_executed"]["high_priority_alerts"] = []
            for doc in high_priority_docs:
                alert_result = self.send_slack_alert(doc)
                automation_results["workflows_executed"]["high_priority_alerts"].append(alert_result)
        
        # Process MEDIUM priority documents (weekly digest)
        medium_priority_docs = [r for r in results if r.classification == PriorityLevel.MEDIUM_PRIORITY]
        if medium_priority_docs:
            digest_result = self.send_weekly_digest(results)
            automation_results["workflows_executed"]["weekly_digest"] = digest_result
        
        # Process LOW priority documents (logging)
        low_priority_docs = [r for r in results if r.classification == PriorityLevel.LOW_PRIORITY]
        if low_priority_docs:
            log_result = self.log_low_priority(results)
            automation_results["workflows_executed"]["low_priority_logging"] = log_result
        
        # Save automation results
        with open("automation_results.json", 'w') as f:
            json.dump(automation_results, f, indent=2)
        
        return automation_results

    def generate_automation_report(self, results: List[ClassificationResult]) -> str:
        """Generate a comprehensive automation report."""
        high_count = len([r for r in results if r.classification == PriorityLevel.HIGH_PRIORITY])
        medium_count = len([r for r in results if r.classification == PriorityLevel.MEDIUM_PRIORITY])
        low_count = len([r for r in results if r.classification == PriorityLevel.LOW_PRIORITY])
        
        report = f"""
Automation Workflow Report
=========================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Document Distribution:
- High Priority (Immediate Alerts): {high_count}
- Medium Priority (Weekly Digest): {medium_count}
- Low Priority (Logged): {low_count}
- Irrelevant (Ignored): {len([r for r in results if r.classification == PriorityLevel.IRRELEVANT])}

Workflows Executed:
"""
        
        if high_count > 0:
            report += f"* {high_count} Slack alerts sent for immediate follow-up\n"
        
        if medium_count > 0:
            report += f"* Weekly digest email prepared with {medium_count} documents\n"
        
        if low_count > 0:
            report += f"* {low_count} documents logged to {self.log_file}\n"
        
        report += f"""
Files Generated:
- classification_results.json: Detailed classification data
- automation_results.json: Workflow execution details
- automation_log.json: Low priority document log

Next Steps:
- Review high priority documents for immediate action
- Monitor medium priority documents for weekly planning
- Archive low priority documents for future reference
"""
        
        return report 