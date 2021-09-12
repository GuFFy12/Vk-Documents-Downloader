import vk_api, requests, re, os, time
from sys import exit

def cls():
    os.system("cls" if os.name=="nt" else "clear")

def log_in():
    if not os.path.exists("data"):
        os.makedirs("data")
    global dl
    global all
    dl = 0
    all = 0
    cls()
    login_str = input("Login: ")
    password_str = input("Password: ")
    vkObj = vk_api.VkApi(login=login_str, password=password_str, auth_handler=auth_handler)
    try:
        vkObj.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        time.sleep(2)
        log_in()
    else:
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
    input("Press Enter to exit.")
    exit()

def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def stat():
    cls()
    print(f"Downloaded: {dl}/{all}")

log_in()
