import os


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
st.info(os.getcwd())

# ==================================================
# HEADER
# ==================================================

st.title("📧 AI Outreach Agent")

st.write(
    "Generate personalized outreach emails using Google Gemini AI."
)

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

if uploaded_file:
    st.write(type(uploaded_file))

    st.write(uploaded_file.name)

    st.write(uploaded_file.size)

    st.write(uploaded_file.getvalue()[:100])

    st.stop()

    st.write("Before Function")

    leads = csv_service.load_uploaded_leads(uploaded_file)

    st.write("After Function")

    st.sidebar.success("CSV Uploaded Successfully ✅")

    st.sidebar.write(f"📄 {uploaded_file.name}")

# ==================================================
# MAIN CONTENT
# ==================================================

if leads:

    st.success(
        f"✅ Total Leads Loaded: {len(leads)}"
    )

    st.subheader("Lead Preview")

    table_data = []

    for lead in leads:

        table_data.append(
            {
                "Name": lead.name,
                "Company": lead.company,
                "Position": lead.position,
                "Industry": lead.industry,
                "Email": lead.email,
            }
        )

    st.dataframe(
        table_data,
        use_container_width=True,
    )

    st.divider()

    generate = st.button(
        "🚀 Generate Emails",
        use_container_width=True,
    )

    if generate:

        agent = OutreachAgent(
            sender_name=sender,
            company=company,
            tone=tone,
            email_length=email_length,
        )

        st.success(
            "Outreach Agent Initialized Successfully ✅"
        )

        st.write("### Agent Configuration")

        st.json(
            {
                "Sender": sender,
                "Company": company,
                "Tone": tone,
                "Length": email_length,
            }
        )

        progress = st.progress(0)

        status = st.empty()

        results = []

        for index, lead in enumerate(leads):

            status.write(
                f"Generating email for {lead.name}..."
            )

            subject = agent.generate_subject(lead)

            email = agent.generate_email(lead)

            results.append(
                {
                    "lead": lead,
                    "subject": subject,
                    "email": email,
                }
            )

            progress.progress(
                (index + 1) / len(leads)
            )

        status.success(
            "✅ All emails generated successfully."
        )

        st.divider()

        st.header("📨 Generated Emails")

        for item in results:

            st.subheader(item["lead"].name)

            st.write(
                f"**Company:** {item['lead'].company}"
            )

            st.write("**Subject:**")

            st.info(item["subject"])

            st.write("**Generated Email:**")

            st.text_area(
                label=f"Email for {item['lead'].name}",
                value=item["email"],
                height=220,
                key=f"email_{item['lead'].email}",
            )

            st.divider()

else:

    st.info("Upload a CSV file to begin.")

# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption("AI Outreach Agent • Version 2 Development")