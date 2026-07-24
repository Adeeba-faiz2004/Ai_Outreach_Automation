import pandas as pd
import streamlit as st


def render_exports(results):

    export_data = []

    for item in results:

        export_data.append(
            {
                "Name": item["lead"].name,
                "Company": item["lead"].company,
                "Email": item["lead"].email,
                "Subject": item["subject"],
                "Generated Email": item["email"],
            }
        )

    export_df = pd.DataFrame(export_data)

    st.download_button(
        label="📥 Download Generated Emails (CSV)",
        data=export_df.to_csv(index=False),
        file_name="generated_emails.csv",
        mime="text/csv",
    )