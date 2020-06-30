from pprint import pprint
import requests
import time

#Получить список групп
#Получить список друзей
#цикл - Получить спис участ групп - Срав участ гр со списк др - Если нет - сохр. если да - пропуст
#Вывести группы

TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
#id = 171691064
id = 23408383

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


friends_list = []
groups_list = []
final_list = []
l = []

friends_list.extend(take_friends(TOKEN, id)["response"]["items"])
set_list_friends = set(friends_list)
pprint(set_list_friends)

groups_list.extend(take_groups(TOKEN, id)["response"]["items"])
pprint(groups_list)


for i in groups_list:
    try:
        l.extend(take_groups_members(TOKEN, i)["response"]["items"])
        set_l = set(l)
        check_friends = set_l.isdisjoint(set_list_friends)
        if check_friends == False:
            final_list.append(i)
        l.clear()
    except KeyError:
        print('ошибка')

print(final_list)

time.sleep(3)

d = []
last_list = []

for i in final_list:
    try:
        time.sleep(3)
        d.append(take_groups_names(TOKEN, i)["response"][0])
        last_list.append({"name":d[0]["name"], "gid":d[0]["id"],
                          "members_count":take_groups_members(TOKEN, i)["response"]["count"]})
        d.clear()
    except KeyError:
        print('ошибка')
pprint(last_list)
