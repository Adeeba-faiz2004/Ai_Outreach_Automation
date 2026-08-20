import streamlit as st

from agent import load_email_history
from utils.reply_tracker import set_replied, get_reply_stats


def render_history(
    sender,
    company,
    tone,
    email_length,
):

    history = load_email_history()

    st.header("📜 Campaign History")

    if not history:
        st.info("No previous campaigns found.")
        return

    # ==================================================
    # REPLY RATE SUMMARY
    # ==================================================
    stats = get_reply_stats(history)

    stat_col1, stat_col2, stat_col3 = st.columns(3)

    with stat_col1:
        st.metric("📨 Total Emails", stats["total"])
    with stat_col2:
        st.metric("💬 Replied", stats["replied"])
    with stat_col3:
        st.metric("📈 Reply Rate", f"{stats['reply_rate']}%")

    st.caption(
        "Reply tracking is manual — mark a lead as \"Replied\" below once "
        "you see their response land in your own inbox."
    )

    st.divider()

    # ==================================================
    # FILTER
    # ==================================================
    filter_choice = st.radio(
        "Show",
        ["All", "Replied", "Not Replied"],
        horizontal=True,
        key="history_filter",
    )

    if filter_choice == "Replied":
        visible_history = [e for e in history if e.get("replied", False)]
    elif filter_choice == "Not Replied":
        visible_history = [e for e in history if not e.get("replied", False)]
    else:
        visible_history = history

    if not visible_history:
        st.info(f"No emails match the \"{filter_choice}\" filter.")
        return

    for index, email in enumerate(reversed(visible_history)):

        # Safe access — purane data mein keys missing ho sakti hain
        recipient_name = email.get("recipient_name", "Unknown")
        recipient_company = email.get("recipient_company", "Unknown")
        recipient_email = email.get("recipient_email", f"unknown_{index}")
        date = email.get("date", "N/A")
        sender_name = email.get("sender", "N/A")
        company_name = email.get("company", "N/A")
        email_tone = email.get("tone", "N/A")
        subject = email.get("subject", "No Subject")
        body = email.get("email", "No content")
        has_replied = email.get("replied", False)
        replied_at = email.get("replied_at")

        badge = "💬 Replied" if has_replied else "⏳ No reply yet"

        with st.expander(
            f"{recipient_name} • {recipient_company} — {badge}"
        ):

            st.write(f"**Date:** {date}")
            st.write(f"**Sender:** {sender_name}")
            st.write(f"**Company:** {company_name}")
            st.write(f"**Tone:** {email_tone}")
            st.write(f"**Recipient Email:** {recipient_email}")

            st.write("**Subject:**")
            st.info(subject)

            st.write("**Email:**")
            st.write(body)

            st.divider()

            reply_col1, reply_col2 = st.columns([3, 1])

            with reply_col1:
                if has_replied and replied_at:
                    st.success(f"Marked as replied on {replied_at}")

            with reply_col2:
                button_label = (
                    "↩️ Undo" if has_replied else "✅ Mark as Replied"
                )

                # Safe unique key
                button_key = f"reply_toggle_{recipient_email}_{index}"

                if st.button(
                    button_label,
                    key=button_key,
                    use_container_width=True,
                ):
                    set_replied(
                        recipient_email,
                        replied=not has_replied,
                    )
                    st.rerun()
