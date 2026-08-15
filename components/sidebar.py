import streamlit as st


def _inject_sidebar_styles():
    """Lightweight branding layer for the sidebar — gives it a
    'product' feel instead of the default Streamlit look."""
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

            /* Sidebar background + base spacing */
            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #F8F8FD 0%, #EFEEFB 100%);
                border-right: 1px solid #E5E4F4;
            }

            /* Brand header block */
            .sb-brand {
                text-align: center;
                padding: 20px 10px 18px 10px;
                border-radius: 16px;
                background: linear-gradient(135deg, #3D33B0 0%, #6D63EE 60%, #FF6B4A 140%);
                color: #ffffff;
                margin-bottom: 18px;
                box-shadow: 0 8px 18px rgba(79, 70, 229, 0.22);
            }
            .sb-brand .sb-logo {
                font-size: 2.2rem;
                line-height: 1;
                margin-bottom: 4px;
            }
            .sb-brand .sb-title {
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 1.08rem;
                font-weight: 800;
                letter-spacing: -0.01em;
                margin: 2px 0 0 0;
            }
            .sb-brand .sb-subtitle {
                font-size: 0.76rem;
                opacity: 0.9;
                margin-top: 2px;
            }
            .sb-brand .sb-badge {
                display: inline-block;
                margin-top: 9px;
                padding: 3px 12px;
                font-size: 0.68rem;
                font-weight: 700;
                letter-spacing: 0.04em;
                text-transform: uppercase;
                background: rgba(255,255,255,0.22);
                border-radius: 999px;
            }

            /* Section labels */
            .sb-section {
                display: flex;
                align-items: center;
                gap: 6px;
                font-size: 0.82rem;
                font-weight: 700;
                color: #3D33B0;
                text-transform: uppercase;
                letter-spacing: 0.03em;
                margin: 4px 0 6px 0;
            }

            /* Footer credit */
            .sb-footer {
                text-align: center;
                font-size: 0.72rem;
                color: #8792A2;
                padding-top: 10px;
                line-height: 1.5;
            }
            .sb-footer a {
                color: #4F46E5;
                text-decoration: none;
                font-weight: 700;
            }

            section[data-testid="stSidebar"] .stButton button {
                border-radius: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    _inject_sidebar_styles()

    # ---------------- Brand Header ----------------
    st.sidebar.markdown(
        """
        <div class="sb-brand">
            <div class="sb-logo">📧</div>
            <div class="sb-title">AI Outreach Agent</div>
            <div class="sb-subtitle">AI-Powered Cold Email Automation</div>
            <div class="sb-badge">Powered by Gemini AI</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------- Upload ----------------
    st.sidebar.markdown('<div class="sb-section">📂 Upload Leads</div>', unsafe_allow_html=True)

    csv_file = st.sidebar.file_uploader(
        "Upload CSV File",
        type=["csv"],
        help="CSV must include columns like Name, Company, Position, Industry, and Email.",
        label_visibility="collapsed",
    )

    if csv_file is not None:
        size_kb = round(csv_file.size / 1024, 1)
        st.sidebar.caption(f"✅ **{csv_file.name}** • {size_kb} KB")
    else:
        st.sidebar.caption("No file uploaded yet — drag & drop a `.csv` above.")

    st.sidebar.divider()

    # ---------------- Sender ----------------
    st.sidebar.markdown('<div class="sb-section">👤 Sender Details</div>', unsafe_allow_html=True)

    sender = st.sidebar.text_input(
        "Sender Name",
        value="Adeeba Faiz",
        key="sender_name",
        help="This name will appear as the sign-off in every generated email.",
    )

    company = st.sidebar.text_input(
        "Company",
        value="AI Outreach Automation",
        key="company_name",
        help="Your company or brand name, referenced by the AI when writing emails.",
    )

    if not sender.strip() or not company.strip():
        st.sidebar.warning("⚠️ Sender name and company are required for personalized emails.")

    st.sidebar.divider()

    # ---------------- AI Settings ----------------
    st.sidebar.markdown('<div class="sb-section">🤖 AI Settings</div>', unsafe_allow_html=True)

    tone = st.sidebar.selectbox(
        "Tone",
        ["Professional", "Friendly", "Persuasive"],
        help="Controls the writing style Gemini uses for every email in this campaign.",
    )

    email_length = st.sidebar.selectbox(
        "Email Length",
        ["Short", "Medium", "Long"],
        help="Short = 2-3 sentences · Medium = a few short paragraphs · Long = fully detailed pitch.",
    )

    tone_icons = {"Professional": "💼", "Friendly": "🙂", "Persuasive": "🔥"}
    length_icons = {"Short": "⚡", "Medium": "📄", "Long": "📚"}
    st.sidebar.caption(
        f"{tone_icons.get(tone, '')} **{tone}** tone  •  {length_icons.get(email_length, '')} **{email_length}** length"
    )

    st.sidebar.divider()

    # ---------------- History ----------------
    st.sidebar.markdown('<div class="sb-section">📜 History</div>', unsafe_allow_html=True)

    show_history = st.sidebar.checkbox(
        "Show Campaign History",
        help="Displays previously generated campaigns saved from earlier sessions.",
    )

    # ---------------- Footer ----------------
    st.sidebar.divider()
    st.sidebar.markdown(
        """
        <div class="sb-footer">
            Built with Streamlit &amp; Google Gemini AI<br/>
            Developed by <a href="#">Adeeba Faiz</a> · v1.0
        </div>
        """,
        unsafe_allow_html=True,
    )

    return (
        csv_file,
        sender,
        company,
        tone,
        email_length,
        show_history,
    )