import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Set your bot token and channel ID as environment variables for security
# For this example, you can replace them directly or set environment variables:
# os.environ["SLACK_BOT_TOKEN"] = "YOUR_BOT_TOKEN"
# os.environ["SLACK_CHANNEL_ID"] = "YOUR_CHANNEL_ID"

slack_token = os.getenv("SLACK_BOT_TOKEN") # Replace with your token
channel_id = os.getenv("SLACK_CHANNEL_ID") # Replace with your channel ID
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
