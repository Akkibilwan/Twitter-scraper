# Twitter Scraper Streamlit App

This Streamlit app scrapes live tweets from Twitter’s web interface using Playwright—no API required.

## Features

- Search by keyword or hashtag  
- Choose how many tweets to scrape (10–500)  
- Extract: handle, text, timestamp, likes, retweets  
- Display results in a table  
- Download as CSV or JSON  
- Optional: Login via saved cookies  
- Optional: Proxy support  

## Files

- `scraper.py` – the Playwright-based scraper module  
- `app.py`     – the Streamlit UI  
- `requirements.txt` – Python dependencies  
- `.streamlit/secrets.toml` – (optional) cookies & proxies via Streamlit Secrets  

## Deploy (no local steps)

1. Push this repo to GitHub (you’re already here!).  
2. Go to [share.streamlit.io](https://share.streamlit.io/) → **New app**.  
3. Select your GitHub repo, branch `main`, and `app.py`.  
4. In Advanced settings set **Build command** to:
