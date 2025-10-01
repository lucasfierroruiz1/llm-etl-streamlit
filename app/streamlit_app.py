import os
import pandas as pd
from supabase import create_client
import streamlit as st
import altair as alt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="LLM ETL Viewer", layout="wide")

# Read Supabase config from .env
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
table = os.getenv("SUPABASE_TABLE", "etl_items")

st.title("Latest records")

if not url or not key:
    st.error("Missing SUPABASE_URL or SUPABASE_ANON_KEY in environment. Check your .env.")
else:
    try:
        client = create_client(url, key)
        res = client.table(table).select("*").order("updated_at", desc=True).execute()
        df = pd.DataFrame(res.data or [])
    except Exception as e:
        st.error(f"Error querying Supabase: {e}")
        df = pd.DataFrame()

    st.dataframe(df, use_container_width=True)

    if not df.empty:
        st.subheader("Count by topic")
        explode = []
        for _, row in df.iterrows():
            topics = row.get("topics", []) or []
            if isinstance(topics, list):
                for t in topics:
                    explode.append({"topic": str(t)})
            else:
                explode.append({"topic": str(topics)})
        tdf = pd.DataFrame(explode)

        if not tdf.empty:
            chart = alt.Chart(tdf).mark_bar().encode(
                x="count():Q",
                y=alt.Y("topic:N", sort="-x")
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No topics available to chart.")

        st.subheader("Items over time")
        if "updated_at" in df.columns:
            df["updated_at"] = pd.to_datetime(df["updated_at"], errors="coerce")
            time_df = df[["title", "updated_at"]].dropna()
            if not time_df.empty:
                chart2 = alt.Chart(time_df).mark_tick().encode(
                    x="updated_at:T",
                    y=alt.Y("title:N", sort=None)
                )
                st.altair_chart(chart2, use_container_width=True)
            else:
                st.info("No valid timestamps to plot yet.")
        else:
            st.info("Column updated_at not found in data.")

