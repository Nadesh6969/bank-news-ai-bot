import os
import requests

# -----------------------
# Step 1: Dummy news
# Replace this with real scraping later
news = """
DBS Bank launches a new SME digital platform to improve financing access.
OCBC expands its digital banking services to include AI-powered investment tools.
UOB announces partnership with fintech startup for real-time payments.
"""

# -----------------------
# Step 2: Summarize function
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
            print("AI API error:", data)
            return "Error: Could not generate summary"
    except Exception as e:
        print("Exception during summarize:", e)
        return "Error: Could not generate summary"

# -----------------------
# Step 3: Post to X (Twitter)
def post_to_x(message):
    url = "https://api.twitter.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {os.environ['X_BEARER_TOKEN']}",
        "Content-Type": "application/json"
    }
    payload = {"text": message}
    try:
        r = requests.post(url, headers=headers, json=payload)
        if r.status_code == 201 or r.status_code == 200:
            print("✅ Tweet posted successfully!")
        else:
            print(f"❌ Failed to post tweet: {r.status_code}, {r.text}")
    except Exception as e:
        print("Exception during post_to_x:", e)

# -----------------------
# Step 4: Run bot
summary = summarize(news)
print("AI Summary:", summary)
if not summary.startswith("Error"):
    post_to_x(summary)
