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
* **n8n Integration** — Prepared for workflow automation and future expansion of automated outreach processes.

---

## 🔮 Future Improvements



* **Reply Tracking** — Track incoming replies and identify which leads responded to each campaign.
* **Automated Follow-ups** — Schedule personalized follow-up emails based on the lead's response status.
* **Advanced Campaign Management** — Allow users to create, pause, resume, and manage multiple outreach campaigns.
* **Email Analytics** — Add detailed metrics such as response rate, delivery rate, and campaign performance.
* **AI-Powered Lead Personalization** — Improve personalization by analyzing company information, job roles, and industry context.
* **n8n Workflow Automation** — Integrate n8n for automated lead processing, follow-ups, notifications, and campaign workflows.
* **Improved Email Deliverability** — Add better sending strategies, validation, and safeguards to improve delivery and reduce spam risk.
* **Enhanced Dashboard** — Introduce more detailed analytics, campaign insights, and performance visualizations.
* **Scalable Database Architecture** — Improve the database layer to support larger datasets and multiple users efficiently.


---

## 👩‍💻 Author

**Adeeba Faiz**

Built as an AI automation project for learning, portfolio development, and real-world outreach automation.
