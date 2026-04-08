import os
import requests

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
        # Check for 'choices' to prevent crash
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            # Print the full API response for debugging
            print("❌ AI API returned an error or unexpected response:")
            print(data)
            return "Error: Could not generate summary"
    except Exception as e:
        print("Exception during summarize:", e)
        return "Error: Could not generate summary"

def post_to_x(message):
    url = "https://api.twitter.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {os.environ['X_BEARER_TOKEN']}",
        "Content-Type": "application/json"
    }
    payload = {"text": message}
    try:
        r = requests.post(url, headers=headers, json=payload)
        if r.status_code in [200, 201]:
            print("✅ Tweet posted successfully!")
        else:
            print(f"❌ Failed to post tweet: {r.status_code}, {r.text}")
    except Exception as e:
        print("Exception during post_to_x:", e)

# Run bot
summary = summarize(news)
print("AI Summary:", summary)
if not summary.startswith("Error"):
    post_to_x(summary)
