import time
import streamlit as st

from agent import OutreachAgent
from services.csv_service import CSVService

from components.sidebar import render_sidebar
from components.analytics import render_analytics
from components.email_cards import render_email_cards
from components.exports import render_exports
from components.history import render_history


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Outreach Agent",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": (
            "**AI Outreach Agent**  \n"
            "AI-powered personalized cold-email generator built with "
            "Streamlit and Google Gemini.  \n"
            "Developed by Adeeba Faiz."
        )
    },
)

# ==================================================
# CUSTOM STYLING
# ==================================================
# A light branding layer on top of Streamlit's defaults — gives the app
# a polished, "product" feel instead of the default framework look.

st.markdown(
    """
    <style>
        /* Hide default Streamlit chrome for a cleaner, branded look */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        .hero {
            background: linear-gradient(90deg, #1F3864 0%, #2E74B5 100%);
            padding: 28px 32px;
            border-radius: 14px;
            color: #ffffff;
            margin-bottom: 18px;
        }
        .hero h1 {
            margin: 0;
            font-size: 2rem;
            font-weight: 700;
        }
        .hero p {
            margin: 6px 0 0 0;
            font-size: 1rem;
            opacity: 0.9;
        }

        .kpi-card {
            background: #ffffff;
            border: 1px solid #e6e9ef;
            border-radius: 12px;
            padding: 16px 18px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            text-align: center;
        }
        .kpi-card .kpi-label {
            font-size: 0.82rem;
            color: #6b7280;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        .kpi-card .kpi-value {
            font-size: 1.7rem;
            font-weight: 700;
            color: #1F3864;
            margin-top: 4px;
        }
        .status-pill {
            display: inline-block;
            padding: 4px 14px;
            border-radius: 999px;
            font-weight: 600;
            font-size: 0.85rem;
        }
        .status-ok      { background: #E6F4EA; color: #1E7E34; }
        .status-warn    { background: #FFF4E5; color: #B8860B; }
        .status-error   { background: #FDEAEA; color: #C0392B; }
        .status-neutral { background: #EDF2FA; color: #2E74B5; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# HERO HEADER
# ==================================================

st.markdown(
    """
    <div class="hero">
        <h1>📧 AI Outreach Agent</h1>
        <p>Generate personalized, high-converting outreach emails at scale using Google Gemini AI.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==================================================
# SESSION STATE INITIALIZATION
# ==================================================

DEFAULT_STATE = {
    "results": [],
    "campaign_status": "Not Started",
    "successful_emails": 0,
    "failed_emails": 0,
    "campaign_time": 0.0,
}

for key, default_value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = default_value


def reset_campaign():
    """Clear all campaign results so the user can start fresh."""
    for key, default_value in DEFAULT_STATE.items():
        st.session_state[key] = default_value


def status_pill(status: str) -> str:
    """Return a small HTML badge styled according to campaign status."""
    if "Completed" in status and "Errors" not in status:
        css_class = "status-ok"
    elif "Generating" in status:
        css_class = "status-warn"
    elif "Failed" in status or "Quota" in status:
        css_class = "status-error"
    elif "Errors" in status:
        css_class = "status-warn"
    else:
        css_class = "status-neutral"
    return f'<span class="status-pill {css_class}">{status}</span>'


def kpi_card(label: str, value) -> str:
    return f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
    """


# ==================================================
# SIDEBAR
# ==================================================

(
    csv_file,
    sender,
    company,
    tone,
    email_length,
    show_history,
) = render_sidebar()

st.sidebar.divider()
if st.sidebar.button("🔄 Reset Campaign", use_container_width=True):
    reset_campaign()
    st.toast("Campaign reset. Ready for a new run.", icon="🔄")
    st.rerun()

# ==================================================
# LOAD CSV
# ==================================================

csv_service = CSVService()
leads = []

if csv_file is not None:
    try:
        leads = csv_service.load_uploaded_leads(csv_file)
    except Exception as e:
        st.error(f"⚠️ Could not read the uploaded CSV: {e}")
        st.stop()

    st.sidebar.success("CSV Uploaded Successfully ✅")
    st.sidebar.write(f"📄 {csv_file.name}  •  {len(leads)} leads")

# ==================================================
# MAIN TABS
# ==================================================

tab_preview, tab_emails, tab_analytics, tab_history = st.tabs(
    ["📋 Preview & Generate", "✉️ Generated Emails", "📊 Analytics", "🕘 History"]
)

# --------------------------------------------------
# TAB 1 — PREVIEW & GENERATE
# --------------------------------------------------
with tab_preview:
    if len(leads) > 0:
        st.success(f"✅ Total Leads Loaded: {len(leads)}")

        preview = [
            {
                "Name": lead.name,
                "Company": lead.company,
                "Position": lead.position,
                "Industry": lead.industry,
                "Email": lead.email,
            }
            for lead in leads
        ]

        st.subheader("📋 Lead Preview")
        st.caption("Verify uploaded leads before generating AI outreach emails.")

        st.dataframe(
            preview,
            use_container_width=True,
            height=280,
            hide_index=True,
        )

        st.divider()
        st.caption("Ready to generate personalized outreach emails?")

        generate = st.button(
            "🚀 Generate Emails",
            use_container_width=True,
            type="primary",
        )

        # ==============================================
        # GENERATE CAMPAIGN
        # ==============================================
        if generate:
            agent = OutreachAgent(
            sender_name=sender,
            company=company,
            tone=tone,
            email_length=email_length,
        )
               
            st.success("Outreach Agent Initialized Successfully ✅")
            st.session_state.campaign_status = "Generating..."

            progress = st.progress(0)
            status = st.empty()
            eta_placeholder = st.empty()

            start_time = time.time()

            st.session_state.results = []
            st.session_state.successful_emails = 0
            st.session_state.failed_emails = 0

            total_leads = len(leads)
            processed = 0 

            

    

            for index, lead in enumerate(leads):

                status.write(f"Generating email for **{lead.name}**...")

                subject, email = agent.generate_outreach(lead)

                # ==========================================
                # GEMINI QUOTA EXHAUSTED
                # ==========================================
                if subject == "QUOTA_EXCEEDED" or email == "QUOTA_EXCEEDED":

                    st.session_state.campaign_time = round(
                        time.time() - start_time,
                        2,
                    )

                    st.session_state.campaign_status = "Gemini Quota Exhausted ⚠️"

                    status.error(
                        """
        ⚠️ Google Gemini API quota has been exhausted.

        No more emails can be generated because the daily free quota has been reached.

        What you can do:

        • Wait until the quota resets.
        • Use another Gemini API key.
        • Enable billing for higher limits.

        Campaign stopped safely.
        """
                    )

                    break

        # ==========================================
        # AI GENERATION FAILED
        # ==========================================
                if subject == "GENERATION_FAILED" or email == "GENERATION_FAILED":

                    st.session_state.failed_emails += 1

                    subject = "Generation Failed"

                    email = (
                        "❌ AI could not generate this email.\n\n"
                        "Possible reasons:\n"
                        "• Internet connection issue\n"
                        "• Gemini API temporarily unavailable\n"
                        "• Invalid API configuration\n"
                        "• Unexpected AI response"
                    )

                elif subject is not None and email is not None:

                    st.session_state.successful_emails += 1

                    agent.save_email(
                        subject,
                        email,
                        lead,
                    )

                else:

                    st.session_state.failed_emails += 1

                    if subject is None:
                        subject = "No Subject Generated"

                    if email is None:
                        email = "⚠️ Email could not be generated."

                st.session_state.results.append(
                    {
                        "lead": lead,
                        "subject": subject,
                        "email": email,
                    }
                )

                processed += 1

                progress.progress(processed / total_leads)

                elapsed = time.time() - start_time

                avg_per_lead = elapsed / processed

                remaining = max(total_leads - processed, 0)

                eta_seconds = round(avg_per_lead * remaining, 1)

                eta_placeholder.caption(
                    f"⏱ Elapsed: {round(elapsed,1)}s • Estimated time remaining: {eta_seconds}s"
                )

            st.session_state.campaign_time = round(
                time.time() - start_time,
                2,
            )

            eta_placeholder.empty()

            if st.session_state.campaign_status == "Gemini Quota Exhausted ⚠️":

                pass

            elif st.session_state.successful_emails == total_leads:

                st.session_state.campaign_status = "Completed ✅"

                status.success(
                    "✅ All emails generated successfully."
                )

                st.toast(
                    "Campaign completed successfully!",
                    icon="✅",
                )

            elif st.session_state.successful_emails == 0:

                st.session_state.campaign_status = "Failed ❌"

                status.error(
                    """
        ❌ Campaign Failed

        No emails could be generated.

        Please check:

        • Gemini API status
        • Internet connection
        • API Key
        • Prompt configuration
        """
                )

                st.toast(
                    "Campaign failed.",
                    icon="❌",
                )

            else:

                st.session_state.campaign_status = "Completed with Errors ⚠️"

                status.warning(
                    f"""
        Campaign completed with some errors.

        ✅ Successful:
        {st.session_state.successful_emails}

        ❌ Failed:
        {st.session_state.failed_emails}
        """
                )

                st.toast(
                    "Campaign completed with warnings.",
                    icon="⚠️",
                )

        else:

            st.info(
                "📂 Upload a CSV file from the sidebar to begin."
            )
    # ==================================================
    # CAMPAIGN SUMMARY (KPI CARDS)
    # ==================================================
    if len(st.session_state.results) > 0 and len(leads) > 0:
        st.divider()
        st.header("📊 Campaign Summary")
        st.caption("Overview of your AI outreach campaign performance.")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(kpi_card("Total Leads", len(leads)), unsafe_allow_html=True)

        with col2:
            st.markdown(
                kpi_card("Emails Generated", st.session_state.successful_emails),
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                kpi_card("Failed Emails", st.session_state.failed_emails),
                unsafe_allow_html=True,
            )

        with col4:
            attempted = st.session_state.successful_emails + st.session_state.failed_emails
            success_rate = (
                round((st.session_state.successful_emails / attempted) * 100)
                if attempted > 0
                else 0
            )
            st.markdown(kpi_card("Success Rate", f"{success_rate}%"), unsafe_allow_html=True)

        with col5:
            st.markdown(
                kpi_card("Campaign Time", f"{st.session_state.campaign_time}s"),
                unsafe_allow_html=True,
            )

        st.write("")
        st.markdown(
            f"**Status:** {status_pill(st.session_state.campaign_status)}",
            unsafe_allow_html=True,
        )
        st.divider()

# --------------------------------------------------
# TAB 2 — GENERATED EMAILS
# --------------------------------------------------
with tab_emails:
    if len(st.session_state.results) > 0:
        render_email_cards(
            st.session_state.results,
            sender,
            company,
            tone,
            email_length,
        )
        st.divider()
        render_exports(st.session_state.results)
    else:
        st.info("📭 No emails generated yet. Upload a CSV and run a campaign from the **Preview & Generate** tab.")

# --------------------------------------------------
# TAB 3 — ANALYTICS
# --------------------------------------------------
with tab_analytics:
    if len(st.session_state.results) > 0:
        render_analytics(
            st.session_state.results,
            st.session_state.successful_emails,
            st.session_state.failed_emails,
        )
    else:
        st.info("📊 Analytics will appear here once a campaign has been run.")

# --------------------------------------------------
# TAB 4 — HISTORY
# --------------------------------------------------
with tab_history:
    if show_history:
        render_history(sender, company, tone, email_length)
    else:
        st.info("🕘 Enable **Show History** from the sidebar to view past campaigns.")

# ==================================================
# FOOTER
# ==================================================

st.divider()
st.caption("📧 AI Outreach Agent • Built with Streamlit & Google Gemini AI • BSCS Final Year Project • Developed by Adeeba Faiz")