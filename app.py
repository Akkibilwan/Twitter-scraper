# app.py
"""
Streamlit UI for Twitter scraper.
"""

import streamlit as st
import pandas as pd
import json
import tempfile
from scraper import TwitterScraper

st.set_page_config(page_title="Twitter Scraper", layout="wide")
st.title("🐦 Twitter Scraper (No API)")

# Sidebar inputs
st.sidebar.header("Search Settings")
keyword      = st.sidebar.text_input("Keyword or Hashtag", value="streamlit")
limit        = st.sidebar.number_input("Number of Tweets", min_value=10, max_value=500, value=50, step=10)
use_headless = st.sidebar.checkbox("Headless Browser", value=True)

# Load cookies/proxies from Streamlit Secrets, if provided
cookies_path = None
if "cookies" in st.secrets:
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    tf.write(st.secrets.cookies["file"].encode()); tf.flush()
    cookies_path = tf.name

proxies_path = None
if "proxies" in st.secrets:
    tp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    tp.write(st.secrets.proxies["list"].encode()); tp.flush()
    proxies_path = tp.name

if st.sidebar.button("Scrape"):
    scraper = TwitterScraper(
        headless=use_headless,
        cookies_path=cookies_path,
        proxies_path=proxies_path
    )
    with st.spinner(f"Scraping {limit} tweets for “{keyword}”…"):
        data = scraper.scrape(keyword, limit)

    if not data:
        st.warning("No tweets found. Try another keyword or adjust settings.")
    else:
        df = pd.DataFrame(data)
        st.success(f"Fetched {len(df)} tweets.")
        st.dataframe(df)

        # Download buttons
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", data=csv, file_name="tweets.csv", mime="text/csv")

        records = df.to_dict(orient="records")
        js = json.dumps(records, indent=2)
        st.download_button("Download JSON", data=js, file_name="tweets.json", mime="application/json")
