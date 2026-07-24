import pandas as pd
import plotly.express as px
import streamlit as st


def render_analytics(results, successful, failed):

    st.subheader("📊 Campaign Analytics")

    if not results:

        st.info("Generate emails to view campaign analytics.")

        return

    col1, col2 = st.columns(2)

    with col1:

        chart_data = pd.DataFrame(
            {
                "Status": ["Successful", "Failed"],
                "Count": [successful, failed],
            }
        )

        fig = px.pie(
        chart_data,
        names="Status",
        values="Count",
        hole=0.45,
        title="Email Generation Status",
        color="Status",
        color_discrete_map={
            "Successful": "#2563EB",   # Blue
            "Failed": "#93C5FD",       # Light Blue
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