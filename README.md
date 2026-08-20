# 🤖 AI Outreach Agent

An AI-powered outreach automation system that generates personalized cold emails using Google Gemini AI, saves campaign history, exports emails to TXT files, and supports sending emails through Gmail SMTP.

---

## 🚀 Features

* Generate personalized outreach emails using AI
* Generate professional email subject lines
* Industry-specific prompt selection
* Load multiple leads from a CSV file
* Save generated emails to JSON
* Export emails as TXT files
* Send emails using Gmail SMTP
* Secure API key and credentials using `.env`
* Campaign summary after execution
* Logging support

---

## 📂 Project Structure

AI-Outreach-Agent/

* app.py
* agent.py
* config.py
* gemini_service.py
* prompts.py
* requirements.txt
* README.md
* data/
* models/
* services/
* logs/

---

## ⚙️ Technologies Used

* Python
* Google Gemini API
* Gmail SMTP
* JSON
* CSV
* python-dotenv

---

## 📥 Installation

Clone the repository:

```bash
git clone <repository-url>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
SENDER_EMAIL=your_email@gmail.com
APP_PASSWORD=your_app_password
```

Run the project:

```bash
python app.py
```

---

## 📌 Current Features



* **CSV Lead Upload** — Upload and process lead data directly through the Streamlit dashboard.
* **AI-Powered Personalization** — Generate personalized outreach emails for individual leads using Google Gemini AI.
* **Custom Email Settings** — Configure sender name, company, tone, and email length.
* **Email Preview** — Review generated emails before sending them.
* **Automated Email Sending** — Send generated outreach emails through SMTP.
* **Campaign Management** — Create and save campaigns for organized outreach.
* **User Authentication** — Secure user registration and login using password hashing.
* **SQLite Database** — Persist users, campaigns, and lead information locally.
* **Campaign Dashboard** — View campaign status, generated emails, and outreach results through a Streamlit interface.
* **Email Export** — Save generated emails for record-keeping and further use.
* **Campaign History** — Store previous campaigns and their associated lead information.
* **n8n Workflow Automation** — Trigger an automated n8n workflow (Webhook → validation → Gmail send → logging) as an alternative delivery path to direct SMTP, selectable per campaign from the dashboard. See `n8n_workflows/outreach_automation.json`.
* **Advanced Campaign Management** — Pause, resume, or mark campaigns as completed directly from the sidebar; paused campaigns cannot generate new emails until resumed.
* **Delivery Performance Analytics** — Dedicated analytics section showing sent/failed/skipped counts, delivery rate %, and a breakdown of emails sent via Direct SMTP vs. the n8n workflow.
* **Reply Tracking (manual)** — Mark any sent email as "Replied" from the Campaign History tab and filter history by reply status, with a live reply-rate metric.
* **Deliverability Safeguards** — Lead lists are automatically checked for invalid email formats and duplicate addresses before any email is generated or sent, with clear warnings shown in the dashboard.

---

## 🔮 Future Improvements

* **Automated Reply Detection** — Currently reply tracking is manual (marked by the user in the History tab). A future version could poll the sender's inbox via IMAP to auto-detect replies, though this requires a persistently running background process rather than a stateless Streamlit session.
* **Automated Follow-ups** — Schedule personalized follow-up emails automatically based on reply status, once automated reply detection exists to trigger them.
* **Deeper AI-Powered Lead Personalization** — Extend the Lead model to optionally accept richer context (e.g. recent company news, pain points) for even more tailored email generation.
* **Scalable Database Architecture** — Move from SQLite to a networked database (e.g. PostgreSQL) to support larger multi-user datasets in a production deployment.

---

## ⚙️ n8n Workflow Setup

1. Import `n8n_workflows/outreach_automation.json` into your n8n instance (n8n.cloud or self-hosted).
2. Open the **Send Email (Gmail)** node and connect your Gmail OAuth2 credential.
3. Activate the workflow and copy its **Production Webhook URL**.
4. Add it to your `.env` file:
   ```env
   N8N_WEBHOOK_URL=https://your-instance.n8n.cloud/webhook/outreach-send
   ```
5. In the dashboard, after generating emails, select **"n8n Automated Workflow"** as the delivery method before sending.

The workflow validates the incoming payload, sends the email through its Gmail node, and returns a structured success/failure response — giving the project a real automation layer that can later be extended (delays, retries, CRM updates, Slack alerts) without touching the Python codebase.


---
## Demo Below
https://www.linkedin.com/posts/adeebafaiz2004_python-ai-automation-ugcPost-7492617378573307904-DLcm/?utm_source=share&utm_medium=member_desktop&rcm=ACoAAGPEAqQBoCSxQE_318ThzYBr6aXm5UmeEww

## 👩‍💻 Author

**Adeeba Faiz**

Built as an AI automation project for learning, portfolio development, and real-world outreach automation.

---

## 📝 Recent Updates (Version 2.1)

* Added n8n workflow automation as a real, working delivery method (previously listed as pending).
* Added Advanced Campaign Management (Pause / Resume / Complete).
* Added Delivery Performance analytics (sent/failed/skipped, delivery rate, method breakdown).
* Added manual Reply Tracking with reply-rate metrics and filtering.
* Added deliverability safeguards (invalid email + duplicate detection before sending).
