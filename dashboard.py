import pandas as pd
import streamlit as st

from agent import OutreachAgent
from services.csv_service import CSVService

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

# ==================================================
# LOAD CSV
# ==================================================

csv_service = CSVService()
leads = []

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

        st.success("Outreach Agent Initialized Successfully ✅")

        progress = st.progress(0)
        status = st.empty()

        results = []

        for index, lead in enumerate(leads):

            status.write(f"Generating email for {lead.name}...")

            subject = agent.generate_subject(lead)
            email = agent.generate_email(lead)

            results.append(
                {
                    "lead": lead,
                    "subject": subject,
                    "email": email,
                }
            )

            progress.progress((index + 1) / len(leads))

        status.success("✅ All emails generated successfully.")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                 "Total Leads",
                 len(leads),
        )

        with col2:
             st.metric(
                 "Emails Generated",
                 len(results),
    )

        with col3:
             success_rate = round(
                    (len(results) / len(leads)) * 100
    )

             st.metric(
                "Success Rate",
                f"{success_rate}%",
    )

        st.divider()

        st.divider()
        st.header("📨 Generated Emails")

        for item in results:

            st.subheader(item["lead"].name)

            st.write(f"**Company:** {item['lead'].company}")

            st.write("**Subject:**")
            st.info(item["subject"])

            st.write("**Generated Email:**")

            st.text_area(
                label=f"Email for {item['lead'].name}",
                value=item["email"],
                height=220,
                key=item["lead"].email,
            )

            st.divider()

else:

    st.info("📂 Upload a CSV file to begin.")

# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption("AI Outreach Agent • BSCS Final Year Project")