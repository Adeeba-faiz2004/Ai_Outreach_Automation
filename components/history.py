import streamlit as st

from agent import OutreachAgent


def render_history(
    sender,
    company,
    tone,
    email_length,
):

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

        return

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