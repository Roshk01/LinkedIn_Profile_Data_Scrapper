# app_blog.py
import os
import streamlit as st
import pandas as pd
from function import generate_articles_from_api, articles_to_dataframe

st.set_page_config(page_title="AI Blog (Gemini)", page_icon="📝", layout="wide")
st.title("AI Blog Generator — API → Gemini")

# read secrets (Cloud UI) and expose GEMINI key to function.py
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

API_ENDPOINT = st.secrets.get("TITLES_API")  # set in Streamlit Secrets
if not API_ENDPOINT:
    st.error("Missing TITLES_API in Streamlit Secrets.")
    st.stop()

# no inputs; just a button
if st.button("Fetch & Generate 10 Articles"):
    try:
        articles = generate_articles_from_api(
            api_url=API_ENDPOINT,
            limit=10,
            length_words=900,
            level="intermediate",
        )
        df = articles_to_dataframe(articles)
        st.success(f"Generated {len(df)} articles.")
        st.dataframe(df[["title", "brief", "slug"]], use_container_width=True, height=420)

        st.download_button(
            "⬇️ Download CSV",
            df.to_csv(index=False).encode("utf-8"),
            file_name="articles.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"Error: {e}")
