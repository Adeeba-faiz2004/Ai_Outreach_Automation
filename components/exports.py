import pandas as pd
import streamlit as st


def render_exports(results):

    generated = []
    failed = []

    for item in results:

        # Successful emails
        if (
            item["email"] != "⚠️ Email could not be generated."
            and not item["email"].startswith("❌")
        ):

            generated.append(
                {
                    "Name": item["lead"].name,
                    "Company": item["lead"].company,
                    "Email": item["lead"].email,
                    "Subject": item["subject"],
                    "Generated Email": item["email"],
                    "Status": (
                        "Sent"
                        if item.get("sent", False)
                        else "Generated"
                    ),
                }
            )

        # Failed emails
        else:

            if item["email"] == "⚠️ Email could not be generated.":

                reason = "AI Generation Failed"

            else:

                reason = item["email"]

            failed.append(
                {
                    "Name": item["lead"].name,
                    "Company": item["lead"].company,
                    "Email": item["lead"].email,
                    "Reason": reason,
                    "Status": "Failed",
                }
            )

    st.subheader("📦 Export Campaign Results")

    st.caption(
        "Download your generated emails or failed leads for future campaigns."
    )

    col1, col2 = st.columns(2)

    # -------------------------------
    # Generated Emails
    # -------------------------------
    with col1:

        if len(generated) > 0:

            generated_df = pd.DataFrame(generated)

            st.download_button(
                label="📥 Export Generated Emails (.csv)",
                data=generated_df.to_csv(index=False),
                file_name="generated_emails.csv",
                mime="text/csv",
                use_container_width=True,
            )

            st.caption(
                f"✅ {len(generated)} email(s) ready"
            )

    # -------------------------------
    # Failed Leads
    # -------------------------------
    with col2:

        if len(failed) > 0:

            failed_df = pd.DataFrame(failed)

            st.download_button(
                label="📥 Export Failed Leads (.csv)",
                data=failed_df.to_csv(index=False),
                file_name="failed_leads.csv",
                mime="text/csv",
                use_container_width=True,
            )

            st.caption(
                f"❌ {len(failed)} failed lead(s)"
            )

        else:

            st.success(
                "🎉 No failed leads in this campaign."
            )