# app_blog.py
import os
import streamlit as st
import pandas as pd

from function import generate_articles

st.set_page_config(page_title="AI Blog (Gemini)", page_icon="📝", layout="wide")
st.title("📝 AI Blog Generator")

# read secrets (Cloud UI) and expose GEMINI key to function.py
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()


st.write("Enter topics (one per line). Format:")
st.code("Title | brief/description (optional)")

user_input = st.text_area(
    "Paste article topics:",
    height=240,
    placeholder=(
        "Python Decorators | intro + examples\n"
        "Async IO in Python\n"
        "Vector Database | basics + usage"
    )
)

length = st.number_input("Words per article", min_value=300, max_value=2000, value=800, step=50)
level = st.selectbox("Audience level", ["beginner", "intermediate", "advanced"], index=1)

if st.button("Generate Articles"):
    if not user_input.strip():
        st.error("Please enter topics.")
        st.stop()

    try:
        articles = generate_articles(
            user_input,
            limit=10,
            length=length,
            level=level
        )

        df = pd.DataFrame(articles)
        st.success(f" Generated {len(df)} articles.")

        # Show summary view
        st.dataframe(df[["title", "brief"]], use_container_width=True, height=420)

        # Full CSV download
        st.download_button(
            "⬇️ Download CSV",
            df.to_csv(index=False).encode("utf-8"),
            file_name="articles.csv",
            mime="text/csv",
        )

        # Optionally show full markdown for first article
        with st.expander("Preview First Article"):
            st.markdown(df.iloc[0]["markdown"])

    except Exception as e:
        st.error(f"Error: {e}")
