
from services.smtp_service import SMTPService
from logs.log import log_info


from models.lead import Lead
from services.csv_service import CSVService
from services.txt_service import TXTService

from agent import OutreachAgent

log_info("AI Outreach Agent Started")

#lead = Lead(
#    name="John",
#    company="Microsoft",
#   position="HR Manager",
#   industry="Healthcare"
#)

csv_service = CSVService()
leads =csv_service.load_leads("data/leads.csv")

#print(leads)


agent = OutreachAgent(
    sender_name="Adeeba Faiz",
    company="ABC Solutions",
    tone="Friendly",
    email_length="Short"
)
smtp_service = SMTPService()
txt_service = TXTService()
emails_generated = 0
txt_files_exported = 0
for lead in leads:

    print("=" * 50)
    print(f"Generating email for {lead.name}")
    print("=" * 50)

    subject = agent.generate_subject(lead)
    if not subject:

           print("Subject generation failed. Skipping this lead.")

           log_info(f"Subject generation failed for {lead.name}")

           continue

    print("\nSubject:")
    print(subject)

    email = agent.generate_email(lead)

    if email:

        print(email)

        agent.save_email(subject, email, lead)

        log_info("Email Generated")

        filename = (
            f"{lead.name.replace(' ', '_')}_"
            f"{lead.company.replace(' ', '_')}_"
            f"{lead.industry}.txt"
        )

        txt_service.save_email(
            filename,
            subject,
            email
        )

        email_sent = smtp_service.send_email(
            recipient_email=lead.email,
            subject=subject,
            body=email,
        )

        if email_sent:
            print("SMTP Email Sent Successfully")
        else:
            print("SMTP Email Failed")

        emails_generated += 1
        txt_files_exported += 1

    else:

        print("Email generation failed")

        log_info(f"Email generation failed for {lead.name}")