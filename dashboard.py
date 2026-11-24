
import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Tennis Sports Analytics",
    page_icon="🎾",
    layout="wide"
)

API = "https://tennis-sports-analytics.onrender.com"


st.title("🎾 Tennis Sports Analytics")
st.caption("Database-powered Tennis Analytics Platform")


@st.cache_data(ttl=30)
def get_data(endpoint):
    response = requests.get(
        f"{API}/{endpoint}",
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def get_filter_options(df, column):
    if column not in df.columns:
        return ["All"]

    values = (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    options = sorted([
        value for value in values.unique()
        if value and value.lower() != "none"
    ])

    return ["All"] + options


try:
    health = get_data("health")
    st.success("API and MySQL Database Connected")

    competitors = get_data("competitors")
    rankings = get_data("rankings?limit=1000")
    competitions = get_data("competitions")
    venues = get_data("venues")

    competitors_df = pd.DataFrame(competitors)
    rankings_df = pd.DataFrame(rankings)
    competitions_df = pd.DataFrame(competitions)
    venues_df = pd.DataFrame(venues)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Competitors", len(competitors_df))
    c2.metric("Rankings", len(rankings_df))
    c3.metric("Competitions", len(competitions_df))
    c4.metric("Venues", len(venues_df))

    st.divider()

    pages = [
        "Overview",
        "Player Rankings",
        "Competitors",
        "Competitions",
        "Venues",
        "SQL Analytics"
    ]

    page = st.sidebar.selectbox(
        "Select Dashboard",
        pages
    )

    # -------------------------------------------------
    # OVERVIEW
    # -------------------------------------------------

    if page == "Overview":

        st.subheader("Top 10 Player Rankings")

        df = rankings_df.copy()

        if not df.empty and "rank" in df.columns:

            df["rank"] = pd.to_numeric(
                df["rank"], errors="coerce"
            )

            df = (
                df.sort_values("rank")
                .head(10)
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            if (
                "competitor_name" in df.columns
                and "points" in df.columns
            ):
                st.subheader("Ranking Points")

                st.bar_chart(
                    df.set_index("competitor_name")["points"]
                )

    # -------------------------------------------------
    # PLAYER RANKINGS
    # -------------------------------------------------

    elif page == "Player Rankings":

        st.subheader("Player Rankings")

        df = rankings_df.copy()

        search = st.text_input(
            "Search player or country"
        )

        if search and not df.empty:

            mask = df.astype(str).apply(
                lambda col: col.str.contains(
                    search,
                    case=False,
                    na=False
                )
            ).any(axis=1)

            df = df[mask]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    # -------------------------------------------------
    # COMPETITORS
    # -------------------------------------------------

    elif page == "Competitors":

        st.subheader("Competitor Directory")

        df = competitors_df.copy()

        if df.empty:
            st.warning("No competitor records found.")

        else:

            search = st.text_input(
                "Search competitor by name or country"
            )

            if search:

                mask = df.astype(str).apply(
                    lambda col: col.str.contains(
                        search,
                        case=False,
                        na=False
                    )
                ).any(axis=1)

                df = df[mask]

            st.write(
                f"Matching competitors: {len(df)}"
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.divider()
            st.subheader("Individual Competitor Details")

            if not df.empty:

                display_df = df.copy()

                display_df["_label"] = (
                    display_df["name"].astype(str)
                    + " | "
                    + display_df["country"].fillna(
                        "Unknown"
                    ).astype(str)
                    + " | "
                    + display_df["competitor_id"].astype(str)
                )

                selected_label = st.selectbox(
                    "Select a competitor",
                    display_df["_label"].tolist()
                )

                selected = display_df[
                    display_df["_label"] == selected_label
                ].iloc[0]

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Player Name",
                    selected["name"]
                )

                col2.metric(
                    "Country",
                    selected.get("country") or "Unknown"
                )

                col3.metric(
                    "Country Code",
                    selected.get("country_code") or "N/A"
                )

                st.write(
                    "**Competitor ID:**",
                    selected["competitor_id"]
                )

                st.write(
                    "**Abbreviation:**",
                    selected.get("abbreviation") or "N/A"
                )

                # Find player's ranking record
                player_rankings = pd.DataFrame()

                if (
                    not rankings_df.empty
                    and "competitor_id" in rankings_df.columns
                ):

                    player_rankings = rankings_df[
                        rankings_df["competitor_id"].astype(str)
                        == str(selected["competitor_id"])
                    ]

                elif (
                    not rankings_df.empty
                    and "competitor_name" in rankings_df.columns
                ):

                    player_rankings = rankings_df[
                        rankings_df["competitor_name"].astype(str)
                        == str(selected["name"])
                    ]

                st.markdown("#### Ranking Information")

                if not player_rankings.empty:

                    ranking = player_rankings.iloc[0]

                    r1, r2, r3, r4 = st.columns(4)

                    r1.metric(
                        "Current Rank",
                        ranking.get("rank", "N/A")
                    )

                    r2.metric(
                        "Points",
                        ranking.get("points", "N/A")
                    )

                    r3.metric(
                        "Movement",
                        ranking.get("movement", "N/A")
                    )

                    r4.metric(
                        "Competitions Played",
                        ranking.get(
                            "competitions_played",
                            "N/A"
                        )
                    )

                    if "ranking_date" in ranking.index:
                        st.write(
                            "**Ranking Date:**",
                            ranking["ranking_date"]
                        )

                else:
                    st.info(
                        "No ranking record found for this competitor."
                    )

    # -------------------------------------------------
    # COMPETITIONS
    # -------------------------------------------------

    elif page == "Competitions":

        st.subheader("Competition Explorer")

        df = competitions_df.copy()

        if df.empty:
            st.warning("No competition records found.")

        else:

            # Create competition level
            if "parent_id" in df.columns:

                parent_values = (
                    df["parent_id"]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

                df["competition_level"] = parent_values.apply(
                    lambda value:
                    "Sub-competition" if value else "Top-level"
                )

            else:
                df["competition_level"] = "Unknown"

            st.markdown("#### Competition Filters")

            f1, f2, f3, f4 = st.columns(4)

            with f1:
                selected_type = st.selectbox(
                    "Competition Type",
                    get_filter_options(df, "type")
                )

            with f2:
                selected_category = st.selectbox(
                    "Category",
                    get_filter_options(df, "category_name")
                )

            with f3:
                selected_gender = st.selectbox(
                    "Gender",
                    get_filter_options(df, "gender")
                )

            with f4:
                selected_level = st.selectbox(
                    "Competition Level",
                    get_filter_options(
                        df,
                        "competition_level"
                    )
                )

            # Apply filters
            filtered = df.copy()

            if selected_type != "All":
                filtered = filtered[
                    filtered["type"].fillna("").astype(str)
                    == selected_type
                ]

            if selected_category != "All":
                filtered = filtered[
                    filtered["category_name"].fillna("").astype(str)
                    == selected_category
                ]

            if selected_gender != "All":
                filtered = filtered[
                    filtered["gender"].fillna("").astype(str)
                    == selected_gender
                ]

            if selected_level != "All":
                filtered = filtered[
                    filtered["competition_level"]
                    == selected_level
                ]

            st.divider()

            m1, m2, m3 = st.columns(3)

            m1.metric(
                "Total Competitions",
                len(df)
            )

            m2.metric(
                "Filtered Competitions",
                len(filtered)
            )

            m3.metric(
                "Top-level Competitions",
                int(
                    (df["competition_level"] == "Top-level").sum()
                )
            )

            st.subheader("Competition Records")

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "Use the filters above to explore competitions "
                "by type, category, gender and hierarchy level."
            )

    # -------------------------------------------------
    # VENUES
    # -------------------------------------------------

    elif page == "Venues":

        st.subheader("Venue Directory")

        st.dataframe(
            venues_df,
            use_container_width=True,
            hide_index=True
        )

    # -------------------------------------------------
    # SQL ANALYTICS
    # -------------------------------------------------

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

        if st.button(
            "Run Analytics",
            type="primary"
        ):

            with st.spinner("Executing SQL query..."):

                result = get_data(
                    f"analytics/{query_id}"
                )

            data = result["data"]
            df = pd.DataFrame(data)

            st.metric(
                "Records Returned",
                result["total_records"]
            )

            if df.empty:

                st.info("No matching records found.")

            else:

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

                numeric = df.select_dtypes(
                    include="number"
                )

                if not numeric.empty:

                    st.subheader(
                        "Analytics Visualization"
                    )

                    chart_column = st.selectbox(
                        "Select metric for chart",
                        numeric.columns
                    )

                    if len(df.columns) > 1:

                        label_column = st.selectbox(
                            "Select category",
                            [
                                column
                                for column in df.columns
                                if column != chart_column
                            ]
                        )

                        chart_df = df.set_index(
                            label_column
                        )

                        st.bar_chart(
                            chart_df[chart_column]
                        )

                    else:

                        st.bar_chart(
                            df[chart_column]
                        )

    # -------------------------------------------------
    # REFRESH
    # -------------------------------------------------

    if st.sidebar.button("Refresh Data"):

        st.cache_data.clear()
        st.rerun()


except Exception as e:

    st.error(f"Dashboard Error: {e}")

    st.info(
        "Check that FastAPI and MySQL are running."
    )
