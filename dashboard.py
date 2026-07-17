import pandas as pd
import streamlit.components.v1 as components
import streamlit as st
import time
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from agent import OutreachAgent
from services.csv_service import CSVService


def create_pdf(subject, email, lead):


    filename = f"{lead.name}_email.pdf"

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Outreach Email</b>", styles["Title"]))

    story.append(Paragraph(f"<b>Name:</b> {lead.name}", styles["Normal"]))
    story.append(Paragraph(f"<b>Company:</b> {lead.company}", styles["Normal"]))
    story.append(Paragraph(f"<b>Email:</b> {lead.email}", styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph(f"<b>Subject:</b> {subject}", styles["Heading2"]))

    story.append(Paragraph(email.replace("\n", "<br/>"), styles["BodyText"]))

    pdf.build(story)

    return filename

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Outreach Agent",
    page_icon="📧",
    layout="wide",
)

st.title("📧 AI Outreach Agent")
st.write("Generate personalized outreach emails using Google Gemini AI.")
st.divider()

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("Campaign Settings")

sender = st.sidebar.text_input(
    "Sender Name",
    "Adeeba Faiz",
)

company = st.sidebar.text_input(
    "Company",
    "ABC Solutions",
)

tone = st.sidebar.selectbox(
    "Tone",
    [
        "Friendly",
        "Professional",
        "Formal",
    ],
)

email_length = st.sidebar.selectbox(
    "Email Length",
    [
        "Short",
        "Medium",
        "Long",
    ],
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Leads CSV",
    type=["csv"],
)
st.sidebar.divider()

show_history = st.sidebar.button("📜 View Campaign History")

# ==================================================
# LOAD CSV
# ==================================================

csv_service = CSVService()
leads = []
# ==================================================
# SESSION STATE
# ==================================================

if "results" not in st.session_state:
    st.session_state.results = []
    
if "campaign_status" not in st.session_state:
    st.session_state.campaign_status = "Not Started" 
       
if "successful_emails" not in st.session_state:
    st.session_state.successful_emails = 0

if "failed_emails" not in st.session_state:
    st.session_state.failed_emails = 0

if uploaded_file is not None:
    try:

        leads = csv_service.load_uploaded_leads(uploaded_file)

    except Exception as e:

        st.error(str(e))

        st.stop()


    st.sidebar.success("CSV Uploaded Successfully ✅")
    st.sidebar.write(f"📄 {uploaded_file.name}")

# ==================================================
# PREVIEW
# ==================================================

if len(leads) > 0:

    st.success(f"✅ Total Leads Loaded: {len(leads)}")

    preview = []

    for lead in leads:

        preview.append(
            {
                "Name": lead.name,
                "Company": lead.company,
                "Position": lead.position,
                "Industry": lead.industry,
                "Email": lead.email,
            }
        )

    st.subheader("Lead Preview")

    st.dataframe(
        preview,
        use_container_width=True,
    )

    st.divider()

    generate = st.button(
        "🚀 Generate Emails",
        use_container_width=True,
    )
    

    # ==============================================
    # GENERATE
    # ==============================================

    if generate:

        agent = OutreachAgent(
            sender_name=sender,
            company=company,
            tone=tone,
            email_length=email_length,
        )
        #st.write(dir(agent))

        st.success("Outreach Agent Initialized Successfully ✅")
        st.session_state.campaign_status = "Generating..."

        progress = st.progress(0)
        status = st.empty()
        start_time = time.time()

        st.session_state.results = []
        
        st.session_state.successful_emails = 0
        st.session_state.failed_emails = 0
        for index, lead in enumerate(leads):

            status.write(f"Generating email for {lead.name}...")

            subject, email = agent.generate_outreach(lead)
            
            # Stop campaign if Gemini quota is exhausted
            if subject == "QUOTA_EXCEEDED" or email == "QUOTA_EXCEEDED":

                st.session_state.campaign_status = "Quota Exceeded ⚠️"

                status.error(
                    "⚠️ Gemini API quota exhausted.\n"
                    "Generation stopped."
            )

                break
            
            # Count success / failure
            if subject is not None and email is not None:
                 st.session_state.successful_emails += 1
                 agent.save_email(
                              subject,
                              email,
                              lead,
)
            else:
                 st.session_state.failed_emails += 1
           
             # Handle failed subject
            if subject is None:
                subject = "No Subject Generated"
             
            # Handle failed email
            if email is None:
                email = "⚠️ Email could not be generated."
            
            
            

            st.session_state.results.append(
                {
                    "lead": lead,
                    "subject": subject,
                    "email": email,
                }
            )

            progress.progress((index + 1) / len(leads))
            end_time = time.time()

        st.session_state.campaign_time = round(
        end_time - start_time,
        2,
)

        if st.session_state.failed_emails == 0:
            st.session_state.campaign_status = "Completed ✅"
            status.success("✅ All emails generated successfully.")
        
    

        elif st.session_state.successful_emails == 0:
            st.session_state.campaign_status = "Failed ❌"
            status.error("❌ No emails could be generated.")

        else:
            st.session_state.campaign_status = "Completed with Errors ⚠️"
            status.warning(
                f"⚠️ {st.session_state.successful_emails} emails generated successfully, "
                f"{st.session_state.failed_emails} failed."
    )
        
else:
    

    st.info("📂 Upload a CSV file to begin.")
    
    
if len(st.session_state.results) > 0 and len(leads) > 0:
    st.divider()
    st.header("📊 Campaign Analytics")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
            st.metric(
                "Total Leads",
                 len(leads),
        )

    with col2:
            st.metric(
                "Emails Generated",
                st.session_state.successful_emails,
)

    with col3:
            st.metric(
                "Campaign Status",
                 st.session_state.campaign_status,
)

    
    with col4:

            
            st.metric(
                "Failed Emails",
                 st.session_state.failed_emails,
    )
    with col5:

        success_rate = round(
            (st.session_state.successful_emails / len(leads)) * 100
    )

    st.metric(
        "Success Rate",
        f"{success_rate}%",
    )
    

        

    st.divider()

        # ==================================================
        # EXPORT GENERATED EMAILS
        # ==================================================

    export_data = []

    for item in st.session_state.results:

            export_data.append(
        {
                    "Name": item["lead"].name,
                    "Company": item["lead"].company,
                    "Email": item["lead"].email,
                    "Subject": item["subject"],
                    "Generated Email": item["email"],
        }
    )

    export_df = pd.DataFrame(export_data)

    st.download_button(
            label="📥 Download Generated Emails (CSV)",
            data=export_df.to_csv(index=False),
            file_name="generated_emails.csv",
            mime="text/csv",
        )
    
    st.divider()    

        

        
    st.header("📨 Generated Emails")

    for item in st.session_state.results:

        st.subheader(item["lead"].name)

        st.write(f"**Company:** {item['lead'].company}")

        st.write("**Subject:**")
        st.info(item["subject"])

        st.write("**Generated Email:**")

        st.text_area(
                label=f"Email for {item['lead'].name}",
                value=item["email"],
                height=220,
                key=f"email_{item['lead'].email}_{hash(item['email'])}",
            )
        components.html(
            
        f"""
        <button id="copyBtn" onclick="
        navigator.clipboard.writeText(`{item['email']}`);
        this.innerHTML='✅ Copied!';
        setTimeout(() => {{
            this.innerHTML='📋 Copy Email';
        }}, 2000);
    ">
        📋 Copy Email
    </button>
    """,
    height=45,
)
        st.download_button(
                label="📄 Download TXT",
                data=item["email"],
                file_name=f"{item['lead'].name}_email.txt",
                mime="text/plain",
                key=f"download_{item['lead'].email}",
            )
        pdf_file = create_pdf(
            item["subject"],
            item["email"],
            item["lead"],
)

        with open(pdf_file, "rb") as file:

            st.download_button(
                label="📑 Download PDF",
                data=file,
                file_name=pdf_file,
                mime="application/pdf",
                key=f"pdf_{item['lead'].email}",
    )
        button_text = (
                "🔄 Retry"
                if item["email"] == "⚠️ Email could not be generated."
                else "✨ Regenerate"
)

        if st.button(
                button_text,
                key=f"regen_{item['lead'].email}",
):
            
            with st.spinner("Regenerating email..."):
                agent = OutreachAgent(
                    sender_name=sender,
                    company=company,
                    tone=tone,
                    email_length=email_length,
)
                new_subject, new_email = agent.generate_outreach(item["lead"])
                
                if new_subject is not None and new_email is not None:

                    for i, result in enumerate(st.session_state.results):

                        if result["lead"].email == item["lead"].email:

                            st.session_state.results[i]["subject"] = new_subject
                            st.session_state.results[i]["email"] = new_email

                            break
                    agent.save_email(
                                    new_subject,
                                    new_email,
                                    item["lead"],
)
                    st.success("✅ Email regenerated successfully!")

                    st.rerun()      
                else:

                    st.error("❌ Retry failed. Please try again.")


    st.divider()
    if show_history:

        agent = OutreachAgent(
        sender_name=sender,
        company=company,
        tone=tone,
        email_length=email_length,
    )

        history = agent.load_email()

        st.header("📜 Campaign History")
        if not history:

            st.info("No previous campaigns found.")
        else:

            for email in reversed(history):

                with st.expander(
                    f"{email['recipient_name']} • {email['recipient_company']}"
            ):

                    st.write(f"**Date:** {email['date']}")
                    st.write(f"**Sender:** {email['sender']}")
                    st.write(f"**Company:** {email['company']}")
                    st.write(f"**Tone:** {email['tone']}")

                    st.write("**Subject:**")
                    st.info(email["subject"])

                    st.write("**Email:**")
                    st.write(email["email"])

# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption("AI Outreach Agent • BSCS Final Year Project")
