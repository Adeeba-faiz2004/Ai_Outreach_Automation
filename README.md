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

* AI Email Generation
* AI Subject Generation
* CSV Lead Management
* JSON Storage
* TXT Export
* SMTP Email Sending

---

## 🔮 Future Improvements

* Streamlit Dashboard
* HTML Email Templates
* Email Tracking
* Analytics Dashboard
* Scheduling
* Multiple AI Providers
* Database Integration

---

## 👩‍💻 Author

**Adeeba Faiz**

Built as an AI automation project for learning, portfolio development, and real-world outreach automation.
