import os

import streamlit as st
import streamlit.components.v1 as components

from agent import OutreachAgent
from services.email_sender import EmailSender
from utils.pdf_generator import create_pdf


@st.dialog("👁 Email Preview")
def preview_email(item, sender, company):

    st.markdown(
    f"""
<div style="padding:22px;
background:#ffffff;
border-radius:14px;
border:1px solid #E5E4F4;
box-shadow:0 4px 14px rgba(79,70,229,0.08);">

<h4 style="color:#4F46E5;margin-top:0;">📧 From</h4>

<b>{sender}</b><br>

{company}

<hr style="border-color:#E5E4F4;">

<h4 style="color:#4F46E5;">📨 To</h4>

<b>{item['lead'].name}</b><br>

{item['lead'].email}

<hr style="border-color:#E5E4F4;">

<h4 style="color:#4F46E5;">📌 Subject</h4>

<b>{item['subject']}</b>

<hr style="border-color:#E5E4F4;">

<div style="line-height:1.8;font-size:16px;">

{item["email"].replace(chr(10), "<br>")}

</div>

</div>
""",
    unsafe_allow_html=True,
)

   


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
        with st.container(border=True):


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

            email_key = f"email_{item['lead'].email}"

            if email_key not in st.session_state:
                st.session_state[email_key] = item["email"]

            st.session_state[email_key] = item["email"]

            st.text_area(
                "",
                key=email_key,
                height=240,
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

            col1, col2, col3, col4, col5, col6 = st.columns(6)

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
                        file_name=os.path.basename(pdf_file),
                        mime="application/pdf",
                        key=f"pdf_{lead.email}",
                    )
            #---------------------------------------------
                    # ==========================================
            # SEND EMAIL
            # ==========================================

            with col4:

               

                can_send = (
                        item["email"] != "⚠️ Email could not be generated."
                        and not item["email"].startswith("❌")
                        and not item.get("sent", False)
                    )

                button_label = (
                            "✅ Sent"
                            if item.get("sent", False)
                            else "📨 Send Email"
                        )

                if st.button(
                        button_label,
                        disabled=not can_send,
                        key=f"send_{item['lead'].email}",
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
                            f"Sending email to {item['lead'].company}..."
                        ):

                            if not email_sender.validate_email(
                                item["lead"].email
                            ):

                                st.error(
                                    f"""
❌ Invalid email address

Recipient:
{item['lead'].email}

Please verify the email before sending.
            """
                                )

                                st.stop()

                            success, message = email_sender.send(
                                recipient=item["lead"].email,
                                subject=item["subject"],
                                body=item["email"],
                            )

                        if success:
                            item["sent"] = True
                            item["failed"] = False

                            st.toast(
                                f"📨 Email sent to {item['lead'].company}",
                                icon="✅",
                            )

                            st.success(
                                f"""
### ✅ Email Submitted

**Recipient:** {item['lead'].email}

**Company:** {item['lead'].company}

**Status:**
{message}

ℹ️ Final delivery depends on the recipient's mail server.
            """
                            )
                            st.rerun()

                        else:

                            st.toast(
                                "❌ Email Sending Failed",
                                icon="❌",
                            )

                            st.error(
                                f"""
### ❌ Email could not be sent

**Recipient:** {item['lead'].email}

**Company:** {item['lead'].company}

**Reason:**

{message}
            """
                            ) 
                            
                                     
            # ==========================================
            #preview_email
            # ==========================================
            with col5:

                if st.button(
                    "👁 Preview",
                    key=f"preview_{item['lead'].email}",
                ):

                    preview_email(
                        item,
                        sender,
                        company,
                    )
            # ==========================================
            # REGENERATE EMAIL
            # ==========================================

            with col6:

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

                            if result["lead"].email == lead.email:

                                result["subject"] = new_subject
                                result["email"] = new_email

                                # Regenerated email is now valid — clear
                                # any stale sent/failed/skipped flags from
                                # a previous attempt so KPIs stay accurate.
                                result["sent"] = False
                                result["failed"] = False
                                result["skipped"] = False

                                break

                        agent.save_email(
                            new_subject,
                            new_email,
                            lead,
                        )
                        st.session_state.successful_emails = sum(
                            1
                            for r in results
                            if (
                                r["email"] != "⚠️ Email could not be generated."
                                and not r["email"].startswith("❌")
                            )
                        )

                        st.session_state.failed_emails = sum(
                            1
                            for r in results
                            if (
                                r["email"] == "⚠️ Email could not be generated."
                                or r["email"].startswith("❌")
                            )
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