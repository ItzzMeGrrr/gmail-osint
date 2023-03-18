import argparse

try:
    import requests
except ImportError:
    print("Please install requests module")
    print("pip install requests")
    exit(1)

parser = argparse.ArgumentParser(description="Get UID from Gmail")
parser.add_argument("email", help="Email address")
args = parser.parse_args()._get_kwargs()

email = args[0][1]


def load_headers():
    with open("request.txt", "r") as f:
        raw_request = f.read()

    # Split the raw request into its component parts
    request_lines = raw_request.split("\n")
    headers = {}
    for line in request_lines[1:]:
        if line == "":
            break
        key, value = line.split(": ")
        headers[key] = value
    return headers


session = requests.Session()

url = "https://people-pa.clients6.google.com/$rpc/google.internal.people.v2.minimal.PeopleApiAutocompleteMinimalService/ListAutocompletions"

headers = load_headers()

data = [
    f"{email}",
    None,
    None,
    ["GMAIL_COMPOSE_WEB_POPULOUS"],
    8,
    None,
    None,
    None,
    ["GMAIL_COMPOSE_WEB_POPULOUS", None, 2],
]


res = session.post(
    url,
    headers=headers,
    json=data,
)

parsed_data = res.json()
email_addr = res.json()[0][0][0]
if email_addr:
    uid = parsed_data[0][0][3][0]
    image_url = parsed_data[0][0][3][3][0][1]
    print(f"""{{"UID":"{uid}","image_url":"{image_url}"}}""")
else:
    print("UID not found")
