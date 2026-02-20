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
def mention_handler(body, say):
    # 'body' contains the complete raw payload as a dictionary
    print("Raw payload:", body) 
    # You can extract specific data, e.g., the user who mentioned the bot
    user_id = body['event']['user'] 
    #say(f"Hello, <@{user_id}>! I received your mention.")
    #say(f"clap clap clap")
    question = body['event']['text'].split('>', 1)[1].strip()
    thread_ts_value = body['event'].get("thread_ts") or body['event']["ts"]
    answer = bot.query(question)
    say(text= f"{answer}", thread_ts=thread_ts_value)

if __name__ == "__main__":
    bot = Ooga()
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()