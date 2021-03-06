from colorama import Fore
from time import sleep
from config import token
from codecs import open
from requests import get
import os


logo = """
       __     _       _     _ _
      / _|   | |     | |   (_) |
__  _| |_ ___| |_ ___| |__  _| |_
\ \/ /  _/ _ \ __/ __| '_ \| | __|
 >  <| ||  __/ || (__| | | | | |_
/_/\_\_| \___|\__\___|_| |_|_|\__|
v1.3                     xstratumm
"""


intro = """
xfetchit uses public VKontakte API (https://vk.com/dev/methods).

Only you are responsible for your actions.
"""


LINK = "https://api.vk.com/method/"


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def donate():
    wallets = """
I will be very grateful for any crypto from you,
thx! :3

BTC 1HzA8mZxksDGNuTMu5sKUottp9S8bv9NKA

ETH 0xe9a30E9c2aa2D72c224e771c316aE9a7F4fdE36A

LTC LKeWWBWSN7JQxBKDx32WQnJYPD77LdNSrx

ZEC t1HvDeXHFtoTBYHbzNpVH5ocLgnannmdhhc

Dash XrFaQBuBK7GKtPyWWEy8vsTguer4qRqNCX

ETC 0x6d5644C78CBB78542c6219E3815ffE7EbEBd88bf

QTUM QeQ9SaJEHJ9uR2Apa9ymonfpAudnamBUuY

TRX TKojkeYBDY74ghqrFrj9dTWziw6y2Mh1CN
"""
    cls()
    print(wallets)


def fetch(offset, group_id):
    r = get(LINK + "groups.getMembers",
        params={"access_token": token, "v": 5.9, "group_id": group_id, "offset": offset, "fields": "contacts"}).json()

    return r


def parse(user, parsed):
    if not "mobile_phone" in user or not user["mobile_phone"]:
        pass

    else:
        user = user["mobile_phone"]

        if user[0] in ["7", "8", "+"]:
            parsed.append(user)


def groupParse(group_id):
    r = get(LINK + "groups.getMembers",
        params={"access_token": token, "v": 5.9, "group_id": group_id, "fields": "contacts"}).json()

    if not "response" in r:
        print("\nInvalid group ID or screen name (or group is private).")
        print("Please check it and try one more time.")

    else:
        cls()
        print("Number of members: " + str(r["response"]["count"]))
        print("\nStarting parsing in 5 seconds.")
        sleep(5)
        cls()
        print("Parsing started.")
        print("It can take some time according to amount of group members.\n")
        print("Wait...")

        users = r["response"]["items"]
        count = r["response"]["count"]
        parsed = []

        for user in users:
            parse(user, parsed)

        if count >= 1000:
            left = count - len(users)

            if left <= 1000:
                r = get(LINK + "groups.getMembers",
                    params={"access_token": token, "v": 5.9, "group_id": group_id, "offset": 1000, "fields": "contacts"}).json()

                for user in r["response"]["items"]:
                    parse(user, parsed)

            else:
                offset = 0

                while left >= 1000:
                    offset += 1000
                    left -= 1000

                    r = fetch(offset, group_id)

                    for user in r["response"]["items"]:
                        parse(user, parsed)

                offset += left

                r = fetch(offset, group_id)

                for user in r["response"]["items"]:
                    parse(user, parsed)

        cls()

        if len(parsed) == 0:
            print("Parsing ended, but " + Fore.RED + "nothing found" + Fore.RESET + ".\nTry another group.")

        else:
            print("Parsing ended. Found: " + str(len(parsed)) + " numbers")
            print("\nSaving results to \"found.txt\"")

            if os.path.isfile("found.txt"):
                f = open("found.txt", 'a', "utf-8")

            else:
                f = open("found.txt", "w", "utf-8")

            for user in parsed:
                f.write(user + "\r\n")

            f.close()


def main():
    cls()
    print(Fore.RED + logo + Fore.RESET + intro + "\n")
    print("Choose:\n\n1) Parse phone numbers\n" + "2) Exit\n" +
            Fore.YELLOW + "3) Donate\n" + Fore.RESET)

    choice = input("> ")

    if choice == "1":
        cls()
        print("Choose:\n\n" + Fore.BLUE + "1) Group" + Fore.RESET + "\n*parses" +
            " all users' phone numbers from specified group\n\n" +
            "2) Exit\n")

        choice = input("> ")

        if choice == "1":
            cls()
            group_id = input(Fore.BLUE + "Enter group ID or its screen name\n" + Fore.RESET + "> ")

            groupParse(group_id)

        elif choice == "2":
            exit(0)

        else:
            print("\nInvalid choice.\nPlease read one more time.")

    elif choice == "2":
        exit(0)

    elif choice == "3":
        donate()
        exit(0)

    else:
        print("\nInvalid choice.\nPlease read one more time.")


if __name__ == "__main__":
    if len(token) < 85:
        print("\nInvalid token.\n\nPlease configure it in\n\"config.py\"")

    else:
        main()
