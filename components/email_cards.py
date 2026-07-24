import streamlit as st
import streamlit.components.v1 as components

from agent import OutreachAgent
from services.email_sender import EmailSender
from utils.pdf_generator import create_pdf


def render_email_cards(
    results,
    sender,
    company,
    tone,
    email_length,
):

    email_sender = EmailSender()

    st.header("📨 Generated Emails")

    for item in results:

        st.markdown("---")

        lead = item["lead"]

        st.markdown(
            f"""
### 👤 {lead.name}

🏢 **Company:** {lead.company}

📧 **Email:** {lead.email}
"""
        )

        # ---------------- SUBJECT ----------------

        st.markdown("#### 📌 Subject")
        st.info(item["subject"])

        # ---------------- EMAIL ----------------

        st.markdown("#### ✉️ Generated Email")

        st.text_area(
            "",
            value=item["email"],
            height=240,
            key=f"email_{lead.email}",
            label_visibility="collapsed",
        )

        # ---------------- PDF ----------------

        pdf_file = create_pdf(
            item["subject"],
            item["email"],
            lead,
        )

        button_text = (
            "🔄 Retry"
            if item["email"] == "⚠️ Email could not be generated."
            else "✨ Regenerate"
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        # ==========================================
        # COPY EMAIL
        # ==========================================

        with col1:

            components.html(
                f"""
                <button onclick="
                    navigator.clipboard.writeText(`{item['email']}`);
                    this.innerHTML='✅ Copied!';
                    setTimeout(() => {{
                        this.innerHTML='📋 Copy Email';
                    }},2000);
                ">
                    📋 Copy Email
                </button>
                """,
                height=45,
            )

        # ==========================================
        # DOWNLOAD TXT
        # ==========================================

        with col2:

            st.download_button(
                "📄 Download TXT",
                data=item["email"],
                file_name=f"{lead.name}_email.txt",
                mime="text/plain",
                key=f"txt_{lead.email}",
            )

        # ==========================================
        # DOWNLOAD PDF
        # ==========================================

        with col3:

            with open(pdf_file, "rb") as file:

                st.download_button(
                    "📑 Download PDF",
                    data=file,
                    file_name=pdf_file,
                    mime="application/pdf",
                    key=f"pdf_{lead.email}",
                )
        #---------------------------------------------
                # ==========================================
        # SEND EMAIL
        # ==========================================

        with col4:

            if st.button(
                "📨 Send Email",
                key=f"send_{lead.email}",
            ):

                # Don't send failed emails
                if (
                    item["email"] == "⚠️ Email could not be generated."
                    or item["email"].startswith("❌")
                ):

                    st.error(
                        "This email was not generated successfully. Please regenerate it first."
                    )

                else:

                    with st.spinner(
                        f"Sending email to {lead.company}..."
                    ):

                        success, message = email_sender.send(
                            recipient=lead.email,
                            subject=item["subject"],
                            body=item["email"],
                        )

                    if success:

                        st.toast(
                            f"📨 Email sent to {lead.company}",
                            icon="✅",
                        )

                        st.success(
                            f"""
### ✅ Email Submitted

**Recipient:** {lead.email}

**Company:** {lead.company}

**Status:**
{message}

ℹ️ Final delivery depends on the recipient's mail server.
"""
                        )

                    else:

                        st.toast(
                            "❌ Email Sending Failed",
                            icon="❌",
                        )

                        st.error(
                            f"""
### Email could not be sent

**Recipient:** {lead.email}

**Company:** {lead.company}

**Reason:**

{message}
"""
                        )
                        # ---------------- Regenerate ----------------

                # ==========================================
        # REGENERATE EMAIL
        # ==========================================

        with col5:

            if st.button(
                button_text,
                key=f"regen_{lead.email}",
            ):

                with st.spinner(
                    f"Regenerating email for {lead.company}..."
                ):

                    agent = OutreachAgent(
                        sender_name=sender,
                        company=company,
                        tone=tone,
                        email_length=email_length,
                    )

                    new_subject, new_email = agent.generate_outreach(
                        lead
                    )

                # --------------------------------------
                # GEMINI QUOTA
                # --------------------------------------
                if (
                    new_subject == "QUOTA_EXCEEDED"
                    or new_email == "QUOTA_EXCEEDED"
                ):

                    st.error(
                        """
⚠️ Gemini quota exhausted.

Please wait until the quota resets
or use another API key.
"""
                    )

                # --------------------------------------
                # AI FAILED
                # --------------------------------------
                elif (
                    new_subject == "GENERATION_FAILED"
                    or new_email == "GENERATION_FAILED"
                ):

                    st.error(
                        """
❌ AI could not regenerate this email.

Possible reasons:

• Internet connection issue
• Gemini API temporarily unavailable
• Invalid API configuration
• Unexpected AI response

Please try again later.
"""
                    )

                # --------------------------------------
                # SUCCESS
                # --------------------------------------
                elif (
                    new_subject is not None
                    and new_email is not None
                ):

                    # Update current card
                    item["subject"] = new_subject
                    item["email"] = new_email

                    # Update session results
                    for result in results:

                        if (
                            result["lead"].email
                            == lead.email
                        ):

                            result["subject"] = new_subject
                            result["email"] = new_email
                            break

                    agent.save_email(
                        new_subject,
                        new_email,
                        lead,
                    )

                    st.toast(
                        "✅ Email regenerated successfully!",
                        icon="✅",
                    )

                    st.rerun()

                # --------------------------------------
                # UNKNOWN ERROR
                # --------------------------------------
                else:

                    st.error(
                        "❌ Regeneration failed. Please try again."
                    )
                        
            # -----------------------------------------
           