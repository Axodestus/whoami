import vk_api
from config import *
import logging


class Friend:
    def __init__(self, user_id, first_name):
        self.user_id = user_id
        self.first_name = first_name
        self.count = None
        self.friends = []


class VkFriendsWalker:
    def __init__(self, vk_login, vk_password):
        self.session = vk_api.VkApi(vk_login, vk_password, scope=2)
        try:
            self.session.auth()
            self.vk = self.session.get_api()
        except vk_api.exceptions.AuthError:
            print("Ayayaya error!")

        # startup information.
        self.interest = "domain, online, city, status"
        self.root_friend = Friend("44274786", "Александр")
        self.has_built = False

        # bfs needed.
        self.terminate_number = 0
        self.done_friends = []
        self.one_friends_data = self.vk.friends.get(user_id=self.root_friend.user_id, fields=self.interest)
        self.file = open("data.txt", "a", encoding="utf-8")

    def get_root_friend(self):
        self.terminate_number = self.terminate_number + 1

        for i, item in enumerate(self.one_friends_data["items"]):
            self.current_friend = Friend(item["id"], item["first_name"])
            self.root_friend.friends.append(self.current_friend)
            self.get_friend(self.current_friend.user_id, self.current_friend)


    def get_friend(self, user_id, root_friend):
        self.terminate_number = self.terminate_number + 1

        self.current_friend = None
        self.has_built = False

        for item in self.one_friends_data["items"]:
            if 'is_closed' in item and item['is_closed']:
                print("[INFO]: CLOSED PROFILE")
                continue

            if not self.has_built:
                for sub_item in self.one_friends_data["items"]:
                    self.current_friend = Friend(sub_item["id"], sub_item["first_name"])
                    root_friend.count = self.one_friends_data["count"]
                    root_friend.friends.append(self.current_friend)
                    print(self.current_friend.first_name)
                self.has_built = True

            if self.terminate_number == 20:
                self.terminate_number = self.terminate_number - 1
                return
            try:
                if not len(root_friend.friends) == root_friend.count:
                    self.one_friends_data = self.vk.friends.get(user_id=user_id, fields=self.interest)
                self.get_friend(self.current_friend.user_id, self.current_friend)
            except vk_api.exceptions.ApiError:
                print("[INFO]: DELETED")
                continue


# def get_friends_concept(self):
#         is_terminate = False
#
#         for item in self.root_friend.friends:
#
#             if item["first_name"] in self.done_friends:
#                 continue
#             if self.terminate_number == 2:
#                 is_terminate = True
#                 self.terminate_number = self.terminate_number - 1
#                 return
#             if 'is_closed ' in item and item['is_closed']:
#                 continue
#
#             #   main  print
#             print(len(self.done_friends))
#             print("[INFO]: Recursion level: ", self.terminate_number)
#             print(item["first_name"])
#             self.file.write("[INFO]: Recursion level: " + str(self.terminate_number) + "\n")
#             self.file.write(item["first_name"] + '\n')
#             #  end main print
#
#             self.done_friends.append("first_name")
#             self.needed_friend = item["id"]
#             try:
#                 self.get_friends_concept()
#             except vk_api.exceptions.ApiError:
#                 print("DELETED")

        # end main loop
        # X save items from file.
        # format print items.
        # build tree. I need make some classes entity concept and that communications.
        # format save items from file or database.

    # def get_friends(self):
    #
    #     # maybe pprint
    #     # print(json.dumps(my_friends, indent=4, sort_keys=True))
    #
    #     for item in self.one_friends_data["items"]:
    #
    #         if 'is_closed' in item and item['is_closed']:
    #             continue
    #
    #         if item["id"] in self.done_friends:
    #             continue
    #
    #         with open("dump.txt", 'a') as file:
    #             format_response = f"{item['first_name']} -> {item['domain']} -> " \
    #                               f"{'online' if item['online'] == 1 else 'offline'} \n\t" \
    #                               f"{item['status'] if 'status' in item else '[INFO]: Empty status'} \n\t" \
    #                               f"{item['city'] if 'city' in item else '[INFO]: Doesnt city'} "
    #
    #             print(str(self.counter) + format_response)
    #         self.done_friends.append(item["id"])
    #         self.needed_friend = item["id"]


    # def get_external_friends():
    #     x = random.randint(1, 100)
    #     time.sleep(x)
    #     print("hello world!!!")

# def start_search(self):
#     """this is simple futures test"""
#
#     executor = ThreadPoolExecutor(20)
#     future = []
#     for i in range(100):
#         e = executor.submit(self.get_external_friends)
#         future.append(e)
#
#     for i in range(1000):
#         time.sleep(1)
#         if future[i].result() == "Completed":
#             print("Completed")


def main():
    vk = VkFriendsWalker(login, password)
    vk.get_root_friend()


if __name__ == '__main__':
    main()
