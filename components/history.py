import streamlit as st

from agent import load_email_history


def render_history(
    sender,
    company,
    tone,
    email_length,
):

    # Reading history is a local file operation and doesn't need an
    # OutreachAgent (which would otherwise require a valid Gemini API
    # key just to open this tab).
    history = load_email_history()

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