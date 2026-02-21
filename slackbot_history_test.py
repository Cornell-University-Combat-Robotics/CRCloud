import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from oogabooga import *

load_dotenv()

slack_token = os.getenv("SLACK_BOT_TOKEN") # Replace with your token
channel_id = os.getenv("YOUR_CHANNEL_ID") # Replace with your channel ID
message_text = "Hello, world! This message was sent using the Python Slack SDK."

client = WebClient(token=slack_token)
app = App(token=os.getenv("SLACK_BOT_TOKEN"))

@app.event("app_mention")
def mention_handler(body, say, client):
    user_id = body['event']['user']
    channel_id = body['event']['channel']

    # Detect thread
    thread_ts_value = body['event'].get("thread_ts") or body['event']["ts"]

    question = body['event']['text'].split('>', 1)[1].strip()

    # thread history
    replies = client.conversations_replies(
        channel=channel_id,
        ts=thread_ts_value
    )

    thread_messages = replies["messages"]

    answer = bot.query(
        user_text=question,
        thread_messages=thread_messages
    )

    say(text=f"<@{user_id}> {answer}", thread_ts=thread_ts_value)

if __name__ == "__main__":
    bot = Ooga()
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()