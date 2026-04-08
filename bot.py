import os
import requests
import tweepy

# Dummy banking news (replace with real scraping later)
news = """
DBS Bank launches a new SME digital platform to improve financing access.
OCBC expands its digital banking services to include AI-powered investment tools.
UOB announces partnership with fintech startup for real-time payments.
"""

def summarize(text):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "user",
                     "content": f"Summarize this banking news into 1-2 short tweetable sentences:\n{text}"}
                ]
            }
        )
        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            print("❌ AI API returned an error:")
            print(data)
            return "Error: Could not generate summary"
    except Exception as e:
        print("Exception during summarize:", e)
        return "Error: Could not generate summary"

def post_to_x(message):
    # OAuth 1.0a authentication
    auth = tweepy.OAuth1UserHandler(
        os.environ["TWITTER_API_KEY"],
        os.environ["TWITTER_API_SECRET"],
        os.environ["TWITTER_ACCESS_TOKEN"],
        os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
    )
    api = tweepy.API(auth)
    try:
        api.update_status(message)
        print("✅ Tweet posted successfully!")
    except Exception as e:
        print("❌ Failed to post tweet:", e)

# Run bot
summary = summarize(news)
print("AI Summary:", summary)
if not summary.startswith("Error"):
    post_to_x(summary)
