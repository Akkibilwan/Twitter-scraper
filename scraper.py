# scraper.py
# Ensure Playwright’s browsers are installed at runtime before we import/play
import subprocess, sys
subprocess.run(
    [sys.executable, "-m", "playwright", "install", "--with-deps"],
    check=True
)

from playwright.sync_api import sync_playwright
import json
import random
from time import sleep

class TwitterScraper:
    def __init__(self, headless: bool = True, cookies_path: str = None, proxies_path: str = None):
        """
        headless: run browser in headless mode
        cookies_path: optional path to JSON file with cookies
        proxies_path: optional path to text file listing proxies (one per line)
        """
        self.headless = headless
        self.cookies = None
        if cookies_path:
            with open(cookies_path, 'r') as f:
                self.cookies = json.load(f)
        self.proxies = []
        if proxies_path:
            with open(proxies_path) as f:
                self.proxies = [line.strip() for line in f if line.strip()]

    def _get_proxy(self):
        """Randomly pick a proxy or return None."""
        return random.choice(self.proxies) if self.proxies else None

    def scrape(self, keyword: str, limit: int = 50):
        """
        Scrape up to `limit` tweets containing `keyword`.
        Returns list of dicts: {handle, text, timestamp, likes, retweets}
        """
        results = []
        with sync_playwright() as p:
            proxy = self._get_proxy()
            browser_args = {}
            if proxy:
                browser_args['proxy'] = {'server': proxy}

            browser = p.chromium.launch(headless=self.headless, **browser_args)
            context = browser.new_context()
            if self.cookies:
                context.add_cookies(self.cookies)
            page = context.new_page()
            page.goto(f"https://twitter.com/search?q={keyword}&f=live")
            sleep(2)  # allow initial load

            last_height = page.evaluate("() => document.body.scrollHeight")
            while len(results) < limit:
                articles = page.query_selector_all("article")
                for a in articles:
                    if len(results) >= limit:
                        break
                    try:
                        handle = a.query_selector("div[dir='ltr'] span").inner_text()
                        text = " ".join([n.inner_text() for n in a.query_selector_all("div[lang]")])
                        ts = a.query_selector("time").get_attribute("datetime")
                        like_sel = a.query_selector("[data-testid='like'] span")
                        rt_sel   = a.query_selector("[data-testid='retweet'] span")
                        likes    = like_sel.inner_text() if like_sel else "0"
                        retweets = rt_sel.inner_text() if rt_sel else "0"
                        results.append({
                            "handle":    handle,
                            "text":      text,
                            "timestamp": ts,
                            "likes":     likes,
                            "retweets":  retweets
                        })
                    except Exception:
                        continue

                # scroll down and wait
                page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                sleep(1)
                new_height = page.evaluate("() => document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            browser.close()
        return results
