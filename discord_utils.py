import requests
import os




def send_discord_message(message):
    webhook_url = os.getenv("WEB_HOOK")
    role_id = os.getenv("ROLE_ID")
    #<@&{role_id}>
    data = {
        "content": f"{message}",
        "allowed_mentions": {
            "roles": [role_id]
        }
    }

    try:
        response = requests.post(webhook_url, json=data)

        if response.status_code == 204:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message: {response.status_code}")
            print(f"Response body: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")