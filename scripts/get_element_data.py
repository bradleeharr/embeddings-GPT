import json
import requests


def load_config(filename="credentials.json"):
    """Load the configuration from a JSON file."""
    with open(filename, "r") as file:
        return json.load(file)


def authenticate(homeserver_url, username, password):
    """Authenticate with the Matrix server and return the access token."""
    login_data = {
        "type": "m.login.password",
        "user": username,
        "password": password
    }
    response = requests.post(f"{homeserver_url}/_matrix/client/r0/login", json=login_data)

    if response.status_code != 200:
        print(f"Received {response.status_code} status code with message: {response.text}")
        exit()

    response_data = response.json()
    if "access_token" not in response_data:
        print("Error logging in:", response_data)
        exit()

    return response_data["access_token"]


def verify_authentication(homeserver_url, access_token, username):
    """Verify that the authentication was successful."""
    response = requests.get(f"{homeserver_url}/_matrix/client/r0/account/whoami",
                            params={"access_token": access_token})

    if response.status_code != 200:
        print(f"Authentication failed with status code {response.status_code}. Message: {response.text}")
        exit()

    whoami_data = response.json()
    if 'user_id' in whoami_data and whoami_data['user_id'] == username:
        print("Successfully authenticated as", whoami_data['user_id'])
    else:
        print("Authentication verification failed!")
        exit()


def fetch_messages(homeserver_url, access_token, room_id):
    """Fetch messages from the Matrix room."""
    since_token = None
    all_messages = []
    chunk_counter = 0

    while True:
        params = {
            "access_token": access_token,
            "from": since_token,
            "dir": "b",
            "limit": 10000
        }

        response = requests.get(f"{homeserver_url}/_matrix/client/r0/rooms/{room_id}/messages", params=params)
        response_data = response.json()

        if "chunk" in response_data:
            all_messages.extend(response_data["chunk"])

            # Save the current chunk to a file
            with open(f"element_data2/chunk_{chunk_counter}.json", "w") as chunk_file:
                json.dump(response_data["chunk"], chunk_file)

            chunk_counter += 1
            since_token = response_data["end"]
        else:
            print("Error fetching messages:", response_data)
            break

        if not response_data["chunk"]:
            break

    return all_messages


def download_element_data():
    config = load_config()
    HOMESERVER_URL = config["homeserver"]
    USERNAME = config["user_id"]
    PASSWORD = config["password"]

    access_token = authenticate(HOMESERVER_URL, USERNAME, PASSWORD)
    verify_authentication(HOMESERVER_URL, access_token, USERNAME)

    ROOM_ID =  "ROOMID" """PLACEHOLDER"""
    all_messages = fetch_messages(HOMESERVER_URL, access_token, ROOM_ID)

    # Printing the last 10 messages as an example
    for message in all_messages[-10:]:
        print(f"{message['sender']}: {message['content']['body']}")


if __name__ == "__main__":
    download_element_data()
