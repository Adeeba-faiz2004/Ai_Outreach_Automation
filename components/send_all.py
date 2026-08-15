import streamlit as st
import time

from services.email_sender import EmailSender

GENERATION_FAILED_MARKER = "⚠️ Email could not be generated."


def _is_generation_failed(item) -> bool:
    return (
        item["email"] == GENERATION_FAILED_MARKER
        or item["email"].startswith("❌")
    )


def _is_sendable(item) -> bool:
    """An item can still be sent if it isn't already sent, wasn't marked
    skipped by a previous run (e.g. invalid email), and its generation
    actually succeeded."""
    return (
        not item.get("sent", False)
        and not item.get("skipped", False)
        and not _is_generation_failed(item)
    )


def render_send_all(results):

    sender = EmailSender()

    generated_ready = sum(
        1
        for item in results
        if not _is_generation_failed(item)
    )

    st.success(
        f"✅ {generated_ready} generated emails are ready."
)

    can_send_any = any(_is_sendable(item) for item in results)

    if "confirm_send_all" not in st.session_state:
        st.session_state.confirm_send_all = False

    if "send_all_ran" not in st.session_state:
        st.session_state.send_all_ran = False

    # First Button — disabled once nothing is left that can be sent
    # (everything is already sent, generation-failed, or permanently
    # skipped due to an invalid email).
    if st.button(
        "🚀 Send All Generated Emails" if can_send_any else "✅ All Emails Sent",
        type="primary",
        use_container_width=True,
        disabled=not can_send_any,
    ):
        st.session_state.confirm_send_all = True

    # Confirmation Box
    if st.session_state.confirm_send_all:

        st.warning(
            "⚠️ You are about to send all generated emails.\n\nPlease confirm to continue."
        )

        col1, col2 = st.columns(2)

        # ------------------------------
        # CONFIRM
        # ------------------------------
        with col1:

            if st.button(
                "✅ Yes, Send Now",
                type="primary",
                use_container_width=True,
            ):

                st.session_state.confirm_send_all = False

                sent = 0
                failed = 0
                skipped = 0

                total = len(results)

                progress = st.progress(0)

                status = st.empty()

                start_time = time.time()

                for index, item in enumerate(results):

                    status.write(
                        f"📨 Sending {index+1}/{total} → {item['lead'].company}"
                    )

                    # Already sent
                    if item.get("sent", False):

                        skipped += 1
                        item["skipped"] = True

                        progress.progress((index + 1) / total)

                        continue

                    # AI generation failed — never attempt to send this one
                    if _is_generation_failed(item):

                        skipped += 1
                        item["skipped"] = True

                        progress.progress((index + 1) / total)

                        continue

                    # Invalid email
                    if not sender.validate_email(item["lead"].email):

                        skipped += 1
                        item["skipped"] = True

                        progress.progress((index + 1) / total)

                        continue

                    success, message = sender.send(
                        recipient=item["lead"].email,
                        subject=item["subject"],
                        body=item["email"],
                    )

                    time.sleep(1)

                    if success:

                        sent += 1

                        item["sent"] = True
                        item["failed"] = False

                    else:

                        failed += 1

                        # Mark it so it shows up correctly in the Failed
                        # KPI/summary instead of silently disappearing.
                        item["failed"] = True

                    progress.progress((index + 1) / total)

                duration = round(
                    time.time() - start_time,
                    1,
                )

                status.empty()
                progress.empty()

                # Remember this run's stats so the summary card below
                # survives the upcoming rerun instead of flashing once.
                st.session_state.send_all_ran = True
                st.session_state.send_all_last_run = {
                    "newly_sent": sent,
                    "newly_failed": failed,
                    "newly_skipped": skipped,
                    "duration": duration,
                }
                

                st.toast(
                    "🎉 Bulk Email Campaign Completed!",
                    icon="✅",
                )
                st.rerun()

        # ------------------------------
        # CANCEL
        # ------------------------------
        with col2:

            if st.button(
                "❌ Cancel",
                use_container_width=True,
            ):

                st.session_state.confirm_send_all = False

                st.rerun()

    # ==================================================
    # PERSISTENT SENT SUMMARY CARD
    # ==================================================
    # Shown any time after "Send All" has been used at least once, and
    # always computed live from `results` so it stays accurate even if
    # the person sends/regenerates individual emails afterwards.
    if st.session_state.send_all_ran:

        total = len(results)
        live_sent = sum(
            1
            for item in results
            if item.get("sent", False)
        )

        live_failed = sum(
            1
            for item in results
            if item.get("failed", False)
        )

        live_skipped = sum(
            1
            for item in results
            if item.get("skipped", False)
        )
        last_run = st.session_state.get("send_all_last_run", {})
        st.session_state.send_summary_time = time.time()
        

        st.divider()
        st.subheader("📊 Sent Summary")

        s_col1, s_col2, s_col3, s_col4 = st.columns(4)

        with s_col1:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">📨</div>
                    <div class="kpi-label">Total Leads</div>
                    <div class="kpi-value">{total}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with s_col2:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">✅</div>
                    <div class="kpi-label">Sent</div>
                    <div class="kpi-value">{live_sent}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with s_col3:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">❌</div>
                    <div class="kpi-label">Failed</div>
                    <div class="kpi-value">{live_failed}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with s_col4:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">⏭️</div>
                    <div class="kpi-label">Skipped</div>
                    <div class="kpi-value">{live_skipped}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if last_run:
            st.caption(
                f"Last run: {last_run.get('newly_sent', 0)} newly sent, "
                f"{last_run.get('newly_failed', 0)} failed, "
                f"{last_run.get('newly_skipped', 0)} skipped "
                f"in {last_run.get('duration', 0)}s."
            )