import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv


load_dotenv()

slack_token = os.getenv("SLACK_BOT_TOKEN") # Replace with your token
channel_id = os.getenv("YOUR_CHANNEL_ID") # Replace with your channel ID
message_text = "Hello, world! This message was sent using the Python Slack SDK."

client = WebClient(token=slack_token)

try:
    response = client.chat_postMessage(
        channel=channel_id,
        text=message_text
    )
    print(f"Message sent: {response['ts']}")
except SlackApiError as e:
    # Print the error details if the API call fails
    print(f"Error sending message: {e.response['error']}")
