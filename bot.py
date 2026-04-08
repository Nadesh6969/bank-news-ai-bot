import requests
import os

# Example banking RSS feeds
feeds = [
    "https://www.dbs.com/newsroom/rss",
    "https://www.ocbc.com/group/media/release/rss.xml",
    "https://www.uobgroup.com/newsroom/rss.xml"
]

def get_news():
    articles = []
    for feed in feeds:
        r = requests.get(feed)
        articles.append(r.text[:1500])
    return "\n".join(articles)

def summarize(text):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user",
                 "content": f"Summarize latest banking news in 2 short tweets:\n{text}"}
            ]
        }
    )
    return response.json()["choices"][0]["message"]["content"]

def post_to_x(tweet):
    url = "https://api.twitter.com/2/tweets"

    headers = {
        "Authorization": f"Bearer {os.environ['X_BEARER_TOKEN']}",
        "Content-Type": "application/json"
    }

    requests.post(url, headers=headers, json={"text": tweet})


news = get_news()
summary = summarize(news)
post_to_x(summary)
