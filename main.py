import argparse
import json
import os

try:
    import requests
    from bs4 import BeautifulSoup
    from colorama import Fore
except ImportError:
    print("Please install required modules")
    print("pip install requests bs4 colorama")
    exit(1)

parser = argparse.ArgumentParser(description="Gmail OSINT")
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("-e", "--email", help="Email address")
group.add_argument("-u", "--uid", help="UID")
parser.add_argument("-f", "--file", help="captured request file")
parser.add_argument(
    "-q",
    "--quiet",
    action="store_true",
    help="Quiet mode. Don't print anything to stdout",
)


args = vars(parser.parse_args())

if args.get("email") and not args.get("file"):
    parser.error("-f/--file is required with -e/--email")

email = args.get("email")
request_file = str(args.get("file"))


# check if windows
if os.name == "nt":
    request_file = request_file.replace("\\", "/")

uid = None
if args.get("uid"):
    uid = args.get("uid")

quiet = args.get("quiet")


def load_headers():
    if not os.path.exists(request_file):
        error = {"error": f"{request_file} not found"}
        print(json.dumps(error))
        exit(1)
    with open(request_file, "r") as f:
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


def get_value_at_index(lst, index_string):
    index_list = index_string.strip("[]").split("][")
    try:
        for index in index_list:
            lst = lst[int(index)]
        return lst
    except (IndexError, ValueError, TypeError):
        return None


def get_uid():
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
    email_addr = get_value_at_index(res.json(), "[0][0][0]")
    if not email_addr:
        error = {"error": "Email not found"}
        print(json.dumps(error))
        exit(1)
    return get_value_at_index(parsed_data, "[0][0][3][0]")


def banner():
    if quiet:
        return
    print(
        f"""{Fore.RED} 

███╗░░░███╗░█████╗░██╗██╗░░░░░██╗░░██╗░█████╗░░██╗░░░░░░░██╗██╗░░██╗
████╗░████║██╔══██╗██║██║░░░░░██║░░██║██╔══██╗░██║░░██╗░░██║██║░██╔╝
██╔████╔██║███████║██║██║░░░░░███████║███████║░╚██╗████╗██╔╝█████═╝░
██║╚██╔╝██║██╔══██║██║██║░░░░░██╔══██║██╔══██║░░████╔═████║░██╔═██╗░
██║░╚═╝░██║██║░░██║██║███████╗██║░░██║██║░░██║░░╚██╔╝░╚██╔╝░██║░╚██╗
╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝
        {Fore.RESET}"""
        + f"\t{Fore.BLUE}- By {Fore.GREEN}@Itzzmegrrr{Fore.RESET}"
    )


banner()


if not uid:
    uid = get_uid()

contrib_url = f"https://www.google.com/maps/contrib/{uid}"

res = requests.get(contrib_url)

soup = BeautifulSoup(res.text, "html.parser")

res_text = res.text
start_index = res_text.find("window.APP_INITIALIZATION_STATE=") + len(
    "window.APP_INITIALIZATION_STATE="
)
end_index = res_text.find(";", start_index)

app_init_state_json = json.loads(res_text[start_index:end_index].strip())

user_json = json.loads(app_init_state_json[3][9].replace(")]}'", ""))

reviews_json = get_value_at_index(user_json, "[24][0]")
reviews = []
if reviews_json:
    for review in reviews_json:
        review_dict = {}
        review_dict["place_name"] = get_value_at_index(review, "[1][2]")
        review_dict["place_address"] = get_value_at_index(review, "[1][3]")
        review_dict["place_type"] = get_value_at_index(review, "[1][4][0]")
        review_dict["place_image"] = get_value_at_index(review, "[1][10][0][6][0]")
        review_dict["place_link"] = get_value_at_index(review, "[1][17][0]")
        review_dict["latitude"] = get_value_at_index(review, "[1][0][2]")
        review_dict["longitude"] = get_value_at_index(review, "[1][0][3]")
        review_dict["review_link"] = get_value_at_index(review, "[0][18]")
        reviews.append(review_dict)

user_meta = get_value_at_index(user_json, "[16]")

stats = {}

stats["points"] = get_value_at_index(user_meta, "[8][1][0]")
stat_info = get_value_at_index(user_meta, "[8][0]")
if stat_info:
    for info in stat_info:
        stats[info[6]] = info[7]

info = {}
info["uid"] = uid
info["name"] = get_value_at_index(user_meta, "[0]")
info["image"] = get_value_at_index(user_meta, "[1][6][0]")
info["contrib_url"] = contrib_url
info["stats"] = stats
info["reviews"] = reviews

user_info = []
user_info.append(info)
print(json.dumps(user_info))
