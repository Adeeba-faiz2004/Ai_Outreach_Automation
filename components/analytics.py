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

    # ==================================================
    # DELIVERY PERFORMANCE (Sent / Failed / Skipped)
    # ==================================================
    st.divider()
    st.subheader("📬 Delivery Performance")

    sent_count = sum(1 for item in results if item.get("sent", False))
    failed_count = sum(1 for item in results if item.get("failed", False))
    skipped_count = sum(1 for item in results if item.get("skipped", False))
    not_yet_sent = len(results) - sent_count - failed_count - skipped_count

    if sent_count + failed_count + skipped_count == 0:

        st.info(
            "No emails have been sent yet. Delivery performance will "
            "appear here after you use \"Send All Generated Emails\"."
        )

    else:

        delivery_rate = (
            round((sent_count / (sent_count + failed_count)) * 100, 1)
            if (sent_count + failed_count) > 0
            else 0
        )

        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

        with kpi_col1:
            st.metric("✅ Sent", sent_count)
        with kpi_col2:
            st.metric("❌ Failed", failed_count)
        with kpi_col3:
            st.metric("⏭️ Skipped", skipped_count)
        with kpi_col4:
            st.metric("📈 Delivery Rate", f"{delivery_rate}%")

        delivery_df = pd.DataFrame({
            "Outcome": ["Sent", "Failed", "Skipped", "Not Yet Sent"],
            "Count": [sent_count, failed_count, skipped_count, not_yet_sent],
        })
        delivery_df = delivery_df[delivery_df["Count"] > 0]

        fig_delivery = px.pie(
            delivery_df,
            names="Outcome",
            values="Count",
            hole=0.45,
            title="Delivery Outcome Breakdown",
            color="Outcome",
            color_discrete_map={
                "Sent": "#16A34A",
                "Failed": "#DC2626",
                "Skipped": "#F59E0B",
                "Not Yet Sent": "#94A3B8",
            },
        )

        st.plotly_chart(fig_delivery, use_container_width=True)

        # Delivery method breakdown (Direct SMTP vs n8n), only shown once
        # at least one email has actually been sent via one of the methods.
        method_counts = {}
        for item in results:
            if item.get("sent", False) and item.get("delivery_method"):
                method = item["delivery_method"]
                method_counts[method] = method_counts.get(method, 0) + 1

        if method_counts:

            method_df = pd.DataFrame({
                "Method": list(method_counts.keys()),
                "Emails Sent": list(method_counts.values()),
            })

            fig_method = px.bar(
                method_df,
                x="Method",
                y="Emails Sent",
                text="Emails Sent",
                title="Emails Sent by Delivery Method",
                color="Method",
                color_discrete_sequence=["#2563EB", "#7C3AED"],
            )

            st.plotly_chart(fig_method, use_container_width=True)