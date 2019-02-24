from colorama import Fore
from time import sleep
from config import token
import codecs
import os
import requests

logo = """
       __     _       _     _ _
      / _|   | |     | |   (_) |
__  _| |_ ___| |_ ___| |__  _| |_
\ \/ /  _/ _ \ __/ __| '_ \| | __|
 >  <| ||  __/ || (__| | | | | |_
/_/\_\_| \___|\__\___|_| |_|_|\__|
v1.0                     xstratumm
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
thx! :з

BTC 1HzA8mZxksDGNuTMu5sKUottp9S8bv9NKA

ETH 0xe9a30E9c2aa2D72c224e771c316aE9a7F4fdE36A

LTC LKeWWBWSN7JQxBKDx32WQnJYPD77LdNSrx

ZEC t1HvDeXHFtoTBYHbzNpVH5ocLgnannmdhhc

Dash XrFaQBuBK7GKtPyWWEy8vsTguer4qRqNCX

ETC 0x6d5644C78CBB78542c6219E3815ffE7EbEBd88bf

QTUM QeQ9SaJEHJ9uR2Apa9ymonfpAudnamBUuY

TRX TKojkeYBDY74ghqrFrj9dTWziw6y2Mh1CN

GNT 0xe9a30E9c2aa2D72c224e771c316aE9a7F4fdE36A

If there's no some cryptocurrency in this list,
but you really want to thank me, pls contact:

https://vk.com/xstratumm
https://twitter.com/xstratumm
"""
    cls()
    print(wallets)

def fetch(offset, group_id):
    r = requests.get(LINK + "groups.getMembers",
        params={"access_token": token, "v": 5.9, "group_id": group_id, "offset": offset, "fields": "contacts"}).json()

    return r

def parse(user, parsed):
    if not "mobile_phone" in user or user["mobile_phone"] == "":
        pass

    else:
        parsed.append(user["mobile_phone"])

def groupParse(group_id):
    r = requests.get(LINK + "groups.getMembers",
        params={"access_token": token, "v": 5.9, "group_id": group_id, "fields": "contacts"}).json()

    if not "response" in r:
        print("\nInvalid group ID or screen name (or group is private).")
        print("Please check it and try one more time.")

    else:
        cls()
        print("Number of members: " + str(r["response"]["count"]))
        print("\nStarting parsing in 3 seconds.")
        sleep(3)
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
                r = requests.get(LINK + "groups.getMembers",
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

        else:
            pass

        cls()

        if len(parsed) == 0:
            print("Parsing ended, but " + Fore.RED + "nothing found" + Fore.RESET + ".\nTry another group.")

        else:
            print("Parsing ended. Found: " + str(len(parsed)) + " numbers")
            print("\nSaving results to \"found.txt\"")

            if os.path.isfile("found.txt") == True:
                f = codecs.open("found.txt", 'a', "utf-8")

            else:
                f = codecs.open("found.txt", "w", "utf-8")

            for user in parsed:
                f.write(user + "\r\n")

            f.close()

def main():
    cls()
    print(Fore.RED + logo + Fore.RESET + intro + "\n")
    print("Choose:\n\n1) Parse phone numbers\n" + "2) Exit\n" +
            Fore.YELLOW + "3) Donate\n" + Fore.RESET)

    chs = input("> ")

    if chs == "1":
        cls()
        print("Choose:\n\n" + Fore.BLUE + "1) Group" + Fore.RESET + "\n*parses" +
            " all users' phone numbers from specified group\n\n" +
            "2) Exit\n")

        chs = input("> ")

        if chs == "1":
            cls()
            group_id = input(Fore.BLUE + "Enter group ID or its screen name\n" + Fore.RESET + "> ")

            groupParse(group_id)

        elif chs == "2":
            exit(0)

        else:
            print("\nInvalid choice.\nPlease read one more time.")

    elif chs == "2":
        exit(0)

    elif chs == "3":
        donate()
        exit(0)

    else:
        print("\nInvalid choice.\nPlease read one more time.")

if __name__ == "__main__":
    if len(token) < 85:
        print("\nInvalid token.\n\nPlease configure it in\n\"config.py\"")

    else:
        main()
