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
    """Call OpenRouter API to summarize banking news."""
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
                    {
                        "role": "user",
                        "content": f"Summarize this banking news into 1-2 short tweetable sentences:\n{text}"
                    }
                ]
            }
        )
        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            print("❌ AI API returned an error or unexpected response:")
            print(data)
            return "Error: Could not generate summary"
    except Exception as e:
        print("Exception during summarize:", e)
        return "Error: Could not generate summary"

def post_to_x(message):
    """Post a tweet using Tweepy (OAuth 1.0a User Context)."""
    try:
        client = tweepy.Client(
            consumer_key=os.environ["TWITTER_API_KEY"],
            consumer_secret=os.environ["TWITTER_API_SECRET"],
            access_token=os.environ["TWITTER_ACCESS_TOKEN"],
            access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
        )
        client.create_tweet(text=message)
        print("✅ Tweet posted successfully!")
    except Exception as e:
        print("❌ Failed to post tweet:", e)

if __name__ == "__main__":
    # Step 1: Summarize the news
    summary = summarize(news)
    print("AI Summary:", summary)

    # Step 2: Post to X if summary was successful
    if not summary.startswith("Error"):
        post_to_x(summary)
