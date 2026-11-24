import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Tennis Sports Analytics",
    page_icon="🎾",
    layout="wide"
)

API = "http://127.0.0.1:8000"

st.title("🎾 Tennis Sports Analytics")
st.caption("Database-powered Tennis Analytics Platform")

@st.cache_data(ttl=30)
def get_data(endpoint):
    r = requests.get(f"{API}/{endpoint}", timeout=15)
    r.raise_for_status()
    return r.json()

try:
    health = get_data("health")
    st.success("API and MySQL Database Connected")

    competitors = get_data("competitors")
    rankings = get_data("rankings?limit=1000")
    competitions = get_data("competitions")
    venues = get_data("venues")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Competitors", len(competitors))
    c2.metric("Rankings", len(rankings))
    c3.metric("Competitions", len(competitions))
    c4.metric("Venues", len(venues))

    st.divider()

    pages = [
        "Overview",
        "Player Rankings",
        "Competitors",
        "Competitions",
        "Venues",
        "SQL Analytics"
    ]

    page = st.sidebar.selectbox("Select Dashboard", pages)

    if page == "Overview":
        st.subheader("Top 10 Player Rankings")
        df = pd.DataFrame(rankings)
        if not df.empty:
            df = df.sort_values("rank", ascending=True).head(10)
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.subheader("Ranking Points")
            st.bar_chart(
                df.set_index("competitor_name")["points"]
            )

    elif page == "Player Rankings":
        df = pd.DataFrame(rankings)
        search = st.text_input("Search player or country")

        if search:
            df = df[
                df.astype(str).apply(
                    lambda col: col.str.contains(
                        search, case=False, na=False
                    )
                ).any(axis=1)
            ]

        st.dataframe(df, use_container_width=True, hide_index=True)

    elif page == "Competitors":
        st.dataframe(
            pd.DataFrame(competitors),
            use_container_width=True,
            hide_index=True
        )

    elif page == "Competitions":
        st.dataframe(
            pd.DataFrame(competitions),
            use_container_width=True,
            hide_index=True
        )

    elif page == "Venues":
        st.dataframe(
            pd.DataFrame(venues),
            use_container_width=True,
            hide_index=True
        )

    elif page == "SQL Analytics":
        st.subheader("22 SQL Business Analytics")

        query_names = [
            "Top 10 Competitors",
            "Complete Player Rankings",
            "Country-wise Competitor Count",
            "Country-wise Average Ranking Points",
            "Country-wise Total Ranking Points",
            "Best Ranking by Country",
            "Ranking Movement Analysis",
            "Ranking Distribution",
            "Competitor Country Details",
            "Competitions by Category",
            "Competitions by Gender",
            "Competitions by Event Type",
            "Complete Competition Details",
            "Venues by Country",
            "Venues by City",
            "Venues by Complex",
            "Complexes Without Venues",
            "Rankings by Ranking Date",
            "Top 3 Competitors Per Country",
            "Competitors Without Ranking Records",
            "Ranking Records Without Competitor Master Record",
            "Overall Database KPI Summary"
        ]

        selected = st.selectbox(
            "Choose Analytics",
            query_names
        )

        query_id = query_names.index(selected) + 1

        if st.button("Run Analytics", type="primary"):
            with st.spinner("Executing SQL query..."):
                result = get_data(f"analytics/{query_id}")

            data = result["data"]
            df = pd.DataFrame(data)

            st.metric("Records Returned", result["total_records"])

            if df.empty:
                st.info("No matching records found.")
            else:
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

                numeric = df.select_dtypes(include="number")

                if not numeric.empty:
                    st.subheader("Analytics Visualization")
                    chart_column = st.selectbox(
                        "Select metric for chart",
                        numeric.columns
                    )

                    if len(df.columns) > 1:
                        label_column = st.selectbox(
                            "Select category",
                            [
                                c for c in df.columns
                                if c != chart_column
                            ]
                        )

                        chart_df = df.set_index(label_column)
                        st.bar_chart(chart_df[chart_column])

                    else:
                        st.bar_chart(df[chart_column])

    if st.sidebar.button("Refresh Data"):
        st.cache_data.clear()
        st.rerun()

except Exception as e:
    st.error(f"Dashboard Error: {e}")
    st.info("Check that FastAPI and MySQL are running.")

