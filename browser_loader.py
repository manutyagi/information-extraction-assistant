from newspaper import Article
import requests

def fetch_page_html(url):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/128.0.0.0 Safari/537.36"
            )
        }
        html = requests.get(url, headers=headers, timeout=10).text

        article = Article(url, browser_user_agent=headers["User-Agent"])
        article.download(input_html=html)
        article.parse()

        return article.text or ""
    except Exception as e:
        print("SCRAPE ERROR:", e)
        return ""
