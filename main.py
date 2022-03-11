from sys import exit

import os
import re
import requests
import time
import vk_api


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    if not os.path.exists("data"):
        os.makedirs("data")

    if os.path.exists("vk_config.v2.json"):
        os.remove("vk_config.v2.json")

    cls()

    login_str = input("Login: ")
    password_str = input("Password: ")
    vk_obj = vk_api.VkApi(login=login_str, password=password_str, auth_handler=auth_handler)
    try:
        vk_obj.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        time.sleep(2)
        main()
    else:
        print("Success login!")
        documents_downloader(vk_obj)


def documents_downloader(vk_obj):
    api = vk_obj.get_api()
    documents = api.docs.get()["items"]

    downloaded = 0
    all_doc_count = len(documents)

    for i in range(len(documents)):
        downloaded += 1
        document = documents[i]

        try:
            r = requests.get(document["url"])
        except:
            continue

        if r.status_code == 200:
            with open("data/" + get_valid_filename(str(document["id"]) + "_" + document["title"]), "wb") as output_file:
                output_file.write(r.content)

        stat(downloaded, all_doc_count)

    if os.path.exists("vk_config.v2.json"):
        os.remove("vk_config.v2.json")

    input("Press Enter to exit.")
    exit()


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def stat(downloaded, all_doc_count):
    cls()
    print(f"Downloaded: {downloaded}/{all_doc_count}")


if __name__ == '__main__':
    main()
