import pandas as pd
import plotly.express as px
import streamlit as st


def render_analytics(results):

    st.subheader("📊 Campaign Analytics")

    if not results:

        st.info("Generate emails to view campaign analytics.")

        return

    col1, col2 = st.columns(2)

    with col1:

        generated = sum(
            1
            for item in results
            if (
                item["email"] != "⚠️ Email could not be generated."
                and not item["email"].startswith("❌")
            )
        )

        failed = sum(
            1
            for item in results
            if (
                item["email"] == "⚠️ Email could not be generated."
                or item["email"].startswith("❌")
            )
        )

        chart_data = pd.DataFrame({
            "Status": [
                "Generated",
                "Failed",
            ],
            "Count": [
                generated,
                failed,
            ],
        })

        fig = px.pie(
            chart_data,
            names="Status",
            values="Count",
            hole=0.45,
            title="Email Generation Status",
            color="Status",
            color_discrete_map={
                "Generated": "#2563EB",
                "Failed": "#DC2626",
            },
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with col2:

        industry_df = pd.DataFrame(
    {
        "Industry": [
            item["lead"].industry
            for item in results
        ]
    }
)

        industry_counts = (
                industry_df.groupby("Industry")
                .size()
                .reset_index(name="Emails")
)

        fig = px.bar(
            industry_counts,
            x="Industry",
            y="Emails",
            text="Emails",
            title="Emails by Industry",
            color="Industry",
            color_discrete_sequence=[
                "#1D4ED8",
                "#2563EB",
                "#3B82F6",
                "#60A5FA",
                "#93C5FD",
    ],
)

        st.plotly_chart(
            fig,
            use_container_width=True,
        )