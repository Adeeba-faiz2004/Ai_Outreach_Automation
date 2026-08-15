import time
import streamlit as st

from agent import OutreachAgent
from services.csv_service import CSVService

from components.sidebar import render_sidebar
from components.analytics import render_analytics
from components.email_cards import render_email_cards
from components.send_all import render_send_all
from components.exports import render_exports
from components.history import render_history
from auth import init_db, authenticate_user, create_user

from auth import (
    init_db,
    authenticate_user,
    create_user,
    create_campaign,
    get_user_campaigns,
    save_lead,
    get_campaign_leads,
)


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
# AUTHENTICATION
# ==================================================

init_db()


def show_login():

    st.markdown(
        """
        <div style="text-align:center; margin-top:60px;">
            <h1>🔐 AI Outreach Agent</h1>
            <p>Login to access your outreach dashboard.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, col, _ = st.columns([1, 2, 1])

    with col:

        login_email = st.text_input(
            "📧 Email",
            placeholder="you@example.com",
            key="login_email",
        )

        login_password = st.text_input(
            "🔑 Password",
            type="password",
            key="login_password",
        )

        if st.button(
            "Login",
            type="primary",
            use_container_width=True,
        ):

            if not login_email or not login_password:
                st.error("Please enter your email and password.")

            else:

                success, user = authenticate_user(
                    login_email,
                    login_password,
                )

                if success:

                    st.session_state.authenticated = True
                    st.session_state.user = user

                    st.rerun()

                else:

                    st.error("Invalid email or password.")

        st.divider()

        st.caption("Don't have an account?")

        if st.button(
            "Create Account",
            use_container_width=True,
        ):
            st.session_state.auth_page = "signup"
            st.rerun()


def show_signup():

    st.markdown(
        """
        <div style="text-align:center; margin-top:60px;">
            <h1>📝 Create Account</h1>
            <p>Create your AI Outreach Agent account.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, col, _ = st.columns([1, 2, 1])

    with col:

        email = st.text_input(
            "📧 Email",
            placeholder="you@example.com",
            key="signup_email",
        )

        password = st.text_input(
            "🔑 Password",
            type="password",
            key="signup_password",
        )

        confirm_password = st.text_input(
            "🔑 Confirm Password",
            type="password",
            key="confirm_password",
        )

        if st.button(
            "Create Account",
            type="primary",
            use_container_width=True,
        ):

            if not email or not password:
                st.error("Email and password are required.")

            elif password != confirm_password:
                st.error("Passwords do not match.")

            elif len(password) < 8:
                st.error(
                    "Password must be at least 8 characters."
                )

            else:

                success, message = create_user(
                    email,
                    password,
                )

                if success:

                    st.success(message)

                    st.session_state.auth_page = "login"

                    st.info(
                        "Account created. You can now log in."
                    )

                else:

                    st.error(message)

        if st.button(
            "← Back to Login",
            use_container_width=True,
        ):
            st.session_state.auth_page = "login"
            st.rerun()


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"


if not st.session_state.authenticated:

    if st.session_state.auth_page == "signup":
        show_signup()
    else:
        show_login()

    st.stop()

# ==================================================
# CUSTOM STYLING
# ==================================================
# A light branding layer on top of Streamlit's defaults — gives the app
# a polished, "product" feel instead of the default framework look.

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

        :root {
            --surface: #ffffff;
            --border: #E5E4F4;
            --text-primary: #1E1B3A;
            --text-muted: #6B7290;

            --primary-700: #3D33B0;
            --primary-600: #4F46E5;
            --primary-500: #6D63EE;

            --accent: #FF6B4A;
            --accent-dark: #E85A3B;

            --success-bg: #E7F8EE;
            --success-text: #15803D;
            --warn-bg: #FFF4E0;
            --warn-text: #B45309;
            --error-bg: #FDECEC;
            --error-text: #C0392B;
            --neutral-bg: #EEF0FB;
            --neutral-text: #4338CA;
        }

        /* Hide default Streamlit chrome for a cleaner, branded look */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        html, body, [class*="css"] {
            color: var(--text-primary);
        }

        h1, h2, h3, .hero h1, .kpi-card .kpi-value, .sb-brand .sb-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* ---------------- HERO ---------------- */
        .hero {
            position: relative;
            overflow: hidden;
            background: linear-gradient(120deg, #3D33B0 0%, #4F46E5 45%, #6D63EE 100%);
            padding: 34px 36px;
            border-radius: 18px;
            color: #ffffff;
            margin-bottom: 22px;
            box-shadow: 0 12px 28px rgba(79, 70, 229, 0.25);
        }
        .hero::after {
            content: "";
            position: absolute;
            top: -60px;
            right: -60px;
            width: 220px;
            height: 220px;
            background: radial-gradient(circle, rgba(255,107,74,0.35) 0%, rgba(255,107,74,0) 70%);
            pointer-events: none;
        }
        .hero h1 {
            position: relative;
            margin: 0;
            font-size: 2.15rem;
            font-weight: 800;
            letter-spacing: -0.02em;
        }
        .hero p {
            position: relative;
            margin: 8px 0 0 0;
            font-size: 1.02rem;
            color: rgba(255,255,255,0.88);
        }
        .hero .hero-badge {
            position: relative;
            display: inline-block;
            margin-top: 14px;
            padding: 5px 14px;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            background: rgba(255, 107, 74, 0.9);
            border-radius: 999px;
        }

        /* ---------------- KPI CARDS ---------------- */
        .kpi-card {
            position: relative;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 16px 18px 16px 20px;
            box-shadow: 0 2px 6px rgba(30, 27, 58, 0.05);
            text-align: left;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .kpi-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(79, 70, 229, 0.14);
        }
        .kpi-card::before {
            content: "";
            position: absolute;
            left: 0;
            top: 14px;
            bottom: 14px;
            width: 4px;
            border-radius: 4px;
            background: linear-gradient(180deg, var(--primary-600), var(--accent));
        }
        .kpi-card .kpi-icon {
            font-size: 1.1rem;
            margin-bottom: 6px;
        }
        .kpi-card .kpi-label {
            font-size: 0.78rem;
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        .kpi-card .kpi-value {
            font-size: 1.75rem;
            font-weight: 800;
            color: var(--primary-700);
            margin-top: 2px;
        }

        /* ---------------- STATUS PILLS ---------------- */
        .status-pill {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 999px;
            font-weight: 700;
            font-size: 0.82rem;
            letter-spacing: 0.01em;
        }
        .status-ok      { background: var(--success-bg); color: var(--success-text); }
        .status-warn    { background: var(--warn-bg); color: var(--warn-text); }
        .status-error   { background: var(--error-bg); color: var(--error-text); }
        .status-neutral { background: var(--neutral-bg); color: var(--neutral-text); }

        /* ---------------- BUTTONS ---------------- */
        div.stButton > button[kind="primary"],
        div.stDownloadButton > button {
            background: linear-gradient(100deg, var(--primary-600), var(--accent));
            border: none;
            color: #fff;
            font-weight: 700;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(255, 107, 74, 0.22);
            transition: transform 0.12s ease, box-shadow 0.12s ease;
        }
        div.stButton > button[kind="primary"]:hover,
        div.stDownloadButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 16px rgba(255, 107, 74, 0.32);
            color: #fff;
        }
        div.stButton > button[kind="secondary"] {
            border-radius: 10px;
            border-color: var(--border);
            font-weight: 600;
        }

        /* ---------------- TABS ---------------- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            border-bottom: 1px solid var(--border);
        }
        .stTabs [data-baseweb="tab"] {
            font-weight: 600;
            color: var(--text-muted);
            padding: 8px 6px;
        }
        .stTabs [aria-selected="true"] {
            color: var(--primary-700) !important;
            border-bottom: 2px solid var(--accent) !important;
        }

        /* ---------------- MISC ---------------- */
        div[data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 10px 14px;
        }
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
        <span class="hero-badge">✦ AI-Powered Campaigns</span>
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


def kpi_card(label: str, value, icon: str = "📌") -> str:
    return f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
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

st.sidebar.markdown(
    f"👤 **Logged in as:**  \n"
    f"{st.session_state.user['email']}"
)

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True,
):
    st.session_state.authenticated = False
    st.session_state.pop("user", None)
    st.session_state.auth_page = "login"
    st.rerun()

st.sidebar.divider()

# ==================================================
# CAMPAIGNS
# ==================================================

st.sidebar.divider()

st.sidebar.subheader("📁 Campaigns")

campaign_name = st.sidebar.text_input(
    "Campaign Name",
    placeholder="e.g. July Outreach",
)

if st.sidebar.button(
    "➕ Create Campaign",
    use_container_width=True,
):

    if campaign_name.strip():

        campaign_id = create_campaign(
            st.session_state.user["id"],
            campaign_name.strip(),
        )

        st.sidebar.success(
            f"Campaign #{campaign_id} created!"
        )

        st.rerun()

    else:

        st.sidebar.warning(
            "Please enter a campaign name."
        )


campaigns = get_user_campaigns(
    st.session_state.user["id"]
)

if campaigns:

    campaign_options = {
        campaign[1]: campaign[0]
        for campaign in campaigns
    }

    selected_campaign_name = st.sidebar.selectbox(
        "📁 Select Campaign",
        options=list(campaign_options.keys()),
        key="selected_campaign_name",
    )

    selected_campaign_id = campaign_options[
        selected_campaign_name
    ]

    st.session_state.selected_campaign_id = (
        selected_campaign_id
    )

else:

    st.session_state.selected_campaign_id = None

    st.sidebar.info(
        "Create a campaign first."
    )
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
            
            st.session_state.send_all_ran = False
            st.session_state.pop("send_all_last_run", None)

            st.session_state.successful_emails = 0
            st.session_state.failed_emails = 0

            # Reset previous campaign state
            st.session_state.confirm_send_all = False

            st.session_state.pop("emails_sent", None)
            st.session_state.pop("emails_failed", None)
            st.session_state.pop("emails_skipped", None)
            st.session_state.successful_emails = 0
            st.session_state.failed_emails = 0

            total_leads = len(leads)
            processed = 0 

            

    

            for index, lead in enumerate(leads):
                current_failed = False

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
                    current_failed = True

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

                        "sent": False,
                        "failed": current_failed,
                        "skipped": False,
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
            st.markdown(kpi_card("Total Leads", len(leads), "👥"), unsafe_allow_html=True)

        with col2:
            st.markdown(
                kpi_card("Emails Generated", st.session_state.successful_emails, "✉️"),
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                kpi_card("Failed Emails", st.session_state.failed_emails, "⚠️"),
                unsafe_allow_html=True,
            )

        with col4:
            attempted = st.session_state.successful_emails + st.session_state.failed_emails
            success_rate = (
                round((st.session_state.successful_emails / attempted) * 100)
                if attempted > 0
                else 0
            )
            st.markdown(kpi_card("Success Rate", f"{success_rate}%", "🎯"), unsafe_allow_html=True)

        with col5:
            st.markdown(
                kpi_card("Campaign Time", f"{st.session_state.campaign_time}s", "⏱️"),
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

        # ---------------- LIVE ANALYTICS ----------------



        results = st.session_state.results

        generated = sum(
            1
            for item in results
            if (
                item["email"] != "⚠️ Email could not be generated."
                and not item["email"].startswith("❌")
            )
        )

        sent = sum(
            1
            for item in results
            if item.get("sent", False)
        )

        failed = sum(
            1
            for item in results
            if item.get("failed", False)
        )

        skipped = sum(
            1
            for item in results
            if item.get("skipped", False)
        )
        
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "📧 Generated",
                generated,
            )

        with col2:
            st.metric(
                "✅ Sent",
                sent,
            )

        with col3:
            st.metric(
                "❌ Failed",
                failed,
            )
        with col4:
            st.metric("⏭️ Skipped", skipped)

       
        st.divider()

        render_email_cards(
            st.session_state.results,
            sender,
            company,
            tone,
            email_length,
        )

        st.divider()

        render_send_all(
            st.session_state.results,
        )

        render_exports(
            st.session_state.results,
        )

    else:

        st.info(
            "📭 No emails generated yet. Upload a CSV and run a campaign from the Preview & Generate tab."
        )
# --------------------------------------------------
# TAB 3 — ANALYTICS
# --------------------------------------------------
with tab_analytics:
    if len(st.session_state.results) > 0:
        render_analytics(
            st.session_state.results,
            
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
st.caption("📧 AI Outreach Agent • Built with Streamlit & Google Gemini AI  • Developed by Adeeba Faiz")