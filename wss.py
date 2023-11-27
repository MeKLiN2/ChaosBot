# wss.py
import json
import websocket
import socket
from colorama import Fore, Style, init
import re

# Initialize colorama
init()

# Constants for file paths of saved responses
CHATROOM_FILE_PATH = "chatroom.txt"
LOGOUT_HEADERS_FILE_PATH = "logout_headers.json"
LOGOUT_PATH = "logout.txt"
LOGIN_HEADERS_FILE_PATH = "login_headers.json"
LOGIN_PATH = "login.txt"
TOKEN_HEADERS_FILE_PATH = "token_headers.json"
TOKEN_FILE_PATH = "token.txt"
ROOM_HEADERS_FILE_PATH = "room_response.json"
ROOM_FILE_PATH = "room.txt"

class Color(object):
    """
    Predefined colorama colors.
    """
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    MAGENTA = Fore.MAGENTA
    BLUE = Fore.BLUE
    WHITE = Fore.WHITE

    B_RED = Style.BRIGHT + RED
    B_GREEN = Style.BRIGHT + GREEN
    B_YELLOW = Style.BRIGHT + YELLOW
    B_CYAN = Style.BRIGHT + CYAN
    B_MAGENTA = Style.BRIGHT + MAGENTA
    B_BLUE = Style.BRIGHT + BLUE

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    RESET = Style.RESET_ALL

def print_colored(*args):
    # Extract the color from the first argument
    color = args[0]

    # Print the colored message
    print("{}{}{}".format(color, " ".join(map(str, args[1:])), Style.RESET_ALL))

# Automatically reset color at the end of each print statement
init(autoreset=True)

# Enable or disable WebSocket trace
enable_websocket_trace = True

if enable_websocket_trace:
    websocket.enableTrace(True)

# Read the token and WebSocket details from the file
with open("wss_details.json", "r") as file:
    wss_details = json.load(file)

# Use the 'result' field as the token
token = wss_details["token"]

# Extract WebSocket details
websocket_url = wss_details["endpoint"]

# Print the original WebSocket URL
print_colored(Fore.MAGENTA, websocket_url)

# Print the original line used to create the WebSocket connection with the actual URL
websocket_connection_line = "ws = websocket.create_connection('{}')".format(websocket_url)
print_colored(Color.B_GREEN, "Creating WebSocket connection with the following line of code:")
print_colored(Color.B_RED, websocket_connection_line)
print_colored(Style.RESET_ALL)

# Connect to the WebSocket
ws = websocket.create_connection(websocket_url)

# Remove ANSI escape codes from the printed line
cleaned_print_line = re.sub(r'\x1b\[\d+m', '', "Connecting to WebSocket URL: {}".format(websocket_url))

# Print the cleaned print line with color
print(Color.B_CYAN + cleaned_print_line + Style.RESET_ALL)

# Function to send a JSON message to the WebSocket
def send_message(message):
    ws.send(json.dumps(message))
    print(Fore.RED + "Sent message: {}".format(json.dumps(message)) + Style.RESET_ALL)

# Function to handle incoming messages
def handle_message(message):
    # Add your logic here to process different types of messages
    print(Fore.GREEN + "Received message: {}".format(json.dumps(message, indent=2)) + Style.RESET_ALL)

# Join the room on the WebSocket
join_message = {
    "tc": "join",
    "req": 1,
    "useragent": "tinychat-client-webrtc-undefined_linux x86_64-2.0.20-420",
    "token": token,
    "room": "cancers",
    "nick": "Chaos_bot"
}
send_message(join_message)

# Main loop to listen for messages
while True:
    try:
        message = ws.recv()
        if not message:
            break

        # Parse the message as JSON
        message_data = json.loads(message)

        # Print trace information if enabled around time of last msg
        if enable_websocket_trace:
            print(Fore.CYAN + "Trace info: {}".format(ws.sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_INFO, 8)) + Style.RESET_ALL)

        handle_message(message_data)

        # Respond to pings
        if message_data.get("tc") == "ping":
            send_message({"tc": "pong", "req": message_data.get("req")})
    except websocket.WebSocketConnectionClosedException:
        print("WebSocket connection closed.")
        break
    except Exception as e:
        print("Error:", e)

# Close the WebSocket connection
ws.close()

