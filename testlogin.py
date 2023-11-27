# testlogin.py
import subprocess
import requests
import json
from bs4 import BeautifulSoup
import time
from tokenapi import get_token
from colorama import Fore, Style, init  # Import colorama for colored printing

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

# Initialize colorama
init()

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

# Set the URL for logout
logout_url = "https://tinychat.com/logout"

# Set the headers for logout
logout_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Cookie": "XSRF-TOKEN=eyJpdiI6Im1wT2hGMXNvUktTaE1Ic0lZc3RsREE9PSIsInZhbHVlIjoieHUxTWVlZThMS1cxXC9DRGVpN284NGdQWFNpeU5uRkp2WGtsMFU3cDh2MU1mWFFVMkNCcldodHRvaERoeHJjTnhwTXRMaXZibXBVaWNnRE5Ha1hmTHVRPT0iLCJtYWMiOiJmYTE5NTI0YzQ0MjgyYWFkYzUzYTg2OTYzOWRiMDk4ZmZhY2M3NDRmMDBhYjlkNTljYmJhMjdhMTA0YjhiNmE4In0%3D; tcsession=392371fc18380c7440423a1418a7a9339f8f798b; sm_dapi_session=1; remember_82e5d2c56bdd0811318f0cf078b78bfc=eyJpdiI6Imp2VzJzeU1zMDVHNXN5N0l0TXR3VFE9PSIsInZhbHVlIjoia1M0bFBUbmFYR1dkeU8xWGRvS0xLNlp4b2JFY0R1dDRMS1wvXC9CWVVCTUtqRUhudnZTQmhVTWdtKzlXQm5uNGVYTzd5alJHNFN2RWRGQ25VbGlnVEdzRTlyTVAxTEJ6bVwvSWkrU0NsSFQzRnc9IiwibWFjIjoiNmYxZmJmODMwZmRhYzgwMDc2NDZkYWU2ODdiODNkMzEwZWU3MjVhMzg0YzI2YzQ2ZDk1ZTI4OTg3YjY1OGIxMiJ9; hash=2cb970db9a52c88454a79dfaec59a9dc; user=raise; pass=6e07933fcd8d45b0f3b985c2eb0f52fa",
    "DNT": "1",
    "Host": "tinychat.com",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "TE": "trailers",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
}

# Create a session to handle cookies
logout_session = requests.Session()

# Send a POST request to logout
logout_response = logout_session.post(logout_url, headers=logout_headers)

# Save the response headers to file
with open(LOGOUT_HEADERS_FILE_PATH, "w") as headers_file:
    json.dump(dict(logout_response.headers), headers_file)

# Save the response to logout.txt
with open(LOGOUT_PATH, "w") as logout_file:
    logout_file.write(logout_response.text)

# Print in bright blue
print_colored(Color.B_BLUE, "Logged out successfully!")

# Read username and password from logpass.txt
with open("logpass.txt", "r") as file:
    lines = file.readlines()
    login_username = lines[0].strip()
    login_password = lines[1].strip()

# Set the URL for login
login_url = "https://tinychat.com/login"

# Set the headers
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "DNT": "1",
    "Host": "tinychat.com",
    "Origin": "https://tinychat.com",
    "Referer": "https://tinychat.com/start?",
    "Upgrade-Insecure-Requests": "1",
}

# Create a session to handle cookies
session = requests.Session()

# Function to extract token from the login page
def extract_token(login_page_content):
    soup = BeautifulSoup(login_page_content, "html.parser")
    token_input = soup.find("input", {"name": "_token"})
    if token_input:
        return token_input["value"]
    return None

# Load the login page to extract the token
login_page_response = session.get(login_url)

# Print or save headers to a file
with open(LOGIN_HEADERS_FILE_PATH, "w") as header_file:
    header_file.write(str(login_page_response.headers))

# Extract the token
token = extract_token(login_page_response.content)

# Set the payload data for login
payload = {
    "login_username": login_username,
    "login_password": login_password,
    "remember": "1",
    "next": "",
    "_token": token,
}

# Perform the login
response = session.post(login_url, headers=headers, data=payload, allow_redirects=False)

# Save the response headers to login_headers.json
login_headers = {"Response Headers ({} kB)".format(len(response.headers) / 1024): {"headers": []}}
for header, value in response.headers.items():
    login_headers["Response Headers ({} kB)".format(len(response.headers) / 1024)]["headers"].append({"name": header, "value": value})

with open(LOGIN_HEADERS_FILE_PATH, "w") as headers_file:
    json.dump(login_headers, headers_file, indent=4)

# Save the response to login.txt
with open(LOGIN_PATH, "w") as login_file:
    login_file.write(response.text)

# Print the request details and data sent for login
print_colored(Color.B_GREEN, "Sending login request to:")
print_colored(Fore.RED, "URL:", login_url)
print_colored(Fore.GREEN, "Headers:", headers)
print_colored(Fore.RED, "Data Sent:", payload)
print_colored(Fore.GREEN, "Response Status Code:", response.status_code)
# print only headers because website_response.text is too much html

# Check if the login was successful (status code 302 indicates redirection)
if response.status_code == 302:
    print_colored(Color.B_GREEN, "Login successful")
    
    # Use subprocess.Popen to run wss.py in the background
    subprocess.Popen(["python", "wss.py"])

    # You can print or use the response.headers to get additional information
    print_colored(Color.B_BLUE, "Headers:")
    print_colored(Color.B_MAGENTA, response.headers)

    # Save cookies and other information for future use in tokenapi.py
    with open(TOKEN_FILE_PATH, "w") as token_file:
        token_file.write(str(session.cookies.get_dict()))
        # Add other information you may need from the response.headers
else:
    print_colored(Fore.RED, "Login failed. Status code:", response.status_code)
    print_colored(Fore.MAGENTA, "Response content:")
    print_colored(Fore.CYAN, response.text)
    print(Style.RESET_ALL)

# Run tokenapi.py to get the token
token = get_token()

# Save the token to a file (optional)
with open("token.txt", "w") as file:
    file.write(token)

