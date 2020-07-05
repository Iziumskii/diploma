from pprint import pprint
import requests
import time
import json

TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
id = 171691064

def take_groups(token, usid):
    response = requests.get(
        'https://api.vk.com/method/groups.get',
        params={
            'access_token': token,
            'user_id': usid,
            'v': 5.103
        }
    )
    print('---')
    return (response.json())

def take_friends(token, usid):
    response = requests.get(
        'https://api.vk.com/method/friends.get',
        params={
            'access_token': token,
            'user_id': usid,
            'v': 5.103
        }
    )
    print('---')
    return (response.json())

def take_groups_members(token, grid):
    response = requests.get(
        'https://api.vk.com/method/groups.getMembers',
        params={
            'access_token': token,
            'group_id': grid,
            #'filter': 'friends',
            'v': 5.103
        }
    )
    print('---')
    return (response.json())

def take_groups_names(token, grid):
    response = requests.get(
        'https://api.vk.com/method/groups.getById',
        params={
            'access_token': token,
            'group_id': grid,
            'v': 5.103
        }
    )
    print('---')
    return (response.json())

def sort_groups(groups_list, friends_list):
    members_list = []
    final_list = []
    for group in groups_list:
        try:
            members_list.extend(take_groups_members(TOKEN, group)["response"]["items"])
            set_members_list = set(members_list)
            if set_members_list.isdisjoint(friends_list) == True:
                final_list.append(group)
        except KeyError:
            print('ошибка')
        members_list.clear()
    return final_list

def create_final_list(final_list):
    time.sleep(3)
    names_list = []
    last_list = []
    for group in final_list:
        try:
            time.sleep(3)
            names_list.append(take_groups_names(TOKEN, group)["response"][0])
            last_list.append({"name": names_list[0]["name"], "gid": names_list[0]["id"],
                              "members_count": take_groups_members(TOKEN, group)["response"]["count"]})
            names_list.clear()
        except KeyError:
            print('ошибка')
    return last_list

def create_frends_list():
    friends_list = []
    friends_list.extend(take_friends(TOKEN, id)["response"]["items"])
    set_list_friends = set(friends_list)
    return set_list_friends

def create_groups_list():
    groups_list = []
    groups_list.extend(take_groups(TOKEN, id)["response"]["items"])
    return groups_list

def create_group_data():
    return create_final_list(sort_groups(create_groups_list(), create_frends_list()))

def create_groups_json_file():
    with open("groups.json", "w") as file:
        json.dump((create_group_data()), file)

create_groups_json_file()