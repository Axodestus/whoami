import random
import threading
from concurrent.futures import ThreadPoolExecutor
import random

import vk_api
from config import *
import json
import time


class VkMessageDownloader:
    def __init__(self, vk_login, vk_password):
        self.session = vk_api.VkApi(vk_login, vk_password, scope=2)
        try:
            self.session.auth()
            self.vk = self.session.get_api()
        except vk_api.exceptions.AuthError:
            print("Aya error!")
            exit(1)
        self.recursion_level = 0

        self.interest = "domain, online, city, status"

        # critical line
        my_friends = self.vk.friends.get(user_id=44274786, fields=self.interest)
        self.one_friends_data = my_friends
        self.terminate_number = 0
        self.done_friends = []
        self.counter = 0
        self.needed_friend = 0

    def get_friends_concept(self):
        """Some comment for pep8 and simple sexy guys"""
        self.terminate_number = self.terminate_number + 1

        for item in self.one_friends_data:
            # build tree
            # save items from file.
            for sub_item in self.one_friends_data:
                # format print items
                # format save items from file or database.
                pass

            if self.terminate_number == 3:
                return

            self.vk.friends.get(user_id=44274786, fields=self.interest)
            self.get_friends_concept()

    def get_friends(self):
        """for this section needs some api simple method.
        I found funny idea for this shit.
        We're can parse Friends list and some information."""
        # print(json.dumps(my_friends, indent=4, sort_keys=True))

        for item in self.one_friends_data["items"]:

            if 'is_closed' in item and item['is_closed']:
                continue

            if item["id"] in self.done_friends:
                continue

            with open("dump.txt", 'a') as file:
                format_response = f"{item['first_name']} -> {item['domain']} -> " \
                                  f"{'online' if item['online'] == 1 else 'offline'} \n\t" \
                                  f"{item['status'] if 'status' in item else '[INFO]: Empty status'} \n\t" \
                                  f"{item['city'] if 'city' in item else '[INFO]: Doesnt city'} "

                print(str(self.counter) + format_response)
            self.done_friends.append(item["id"])
            self.needed_friend = item["id"]
            self.counter = self.counter + 1

    def get_external_friends(self):
        x = random.randint(1, 100)
        time.sleep(x)
        print("hello world!!!")

    def start_search(self):
        executor = ThreadPoolExecutor(20)
        future = []
        for i in range(100):
            e = executor.submit(self.get_external_friends)
            future.append(e)

        for i in range(1000):
            time.sleep(1)
            if future[i].result() == "Completed":
                print("Completed")


def main():
    # vk_session = vk_api.VkApi(login, password)
    # vk_session.auth()
    #
    # # vk is primary variable.
    # vk = vk_session.get_api()
    vk = VkMessageDownloader(login, password)
    # is_completed = vk.start_search()
    # if is_completed:
    #     print("Done")
    vk.get_friends()
    # vk.start_search()


if __name__ == '__main__':
    main()

