import vk_api, requests, re, os
from sys import exit

def cls():
    os.system("cls" if os.name=="nt" else "clear")

def brexit():
    print()
    input(f"Press Enter to exit.")
    cls()
    exit()

checked = 0
dl = 0
if not os.path.exists("data"):
    os.makedirs("data")
def log_in():
    global dl
    global all
    cls()
    login_str = input(f"Login: ")
    password_str = input(f"Password: ")
    vkObj = vk_api.VkApi(login=login_str, password=password_str)
    try:
        vkObj.auth()
    except:
        print("Invlaid login or password. You disable 2fa?")
        brexit()
    print("Success login!")
    api = vkObj.get_api()
    documents = api.docs.get()["items"]
    all = len(documents)
    for i in range(len(documents)):
        el = documents[i]
        r = requests.get(el["url"])
        if r.status_code == 200:
            with open("data/" + get_valid_filename(str(el["id"]) + "_" + el["title"]), "wb") as output_file:
                output_file.write(r.content)
        dl += 1
        stat()
    brexit()

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def stat():
    cls()
    print(f"Downloaded: {dl}/{all}")

log_in()