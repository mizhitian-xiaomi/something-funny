import requests


def get_branches(data):
    nameList = []
    for branch in data:
        name = branch['name']
        if name != 'master':
            nameList.append(name)
    return nameList


# 查询gitlab API文档
url = 'https://gitlab.com/api/v4/projects/13020942/repository/branches?private_token=1AMA7UwiNgNKBHpRTVS-&page=1&per_page=50'

# # pre_page：每页显示
# params = {
#     'page': 1,
#     'pre_page': 50
# }

r = requests.get(url)
# respond

data = r.json()

# print(r.headers['content-type'])
# print(data)


cli = input('input your option:')
while cli != 'exit':

    if cli == 'git branch -a':
        branch_data = get_branches(data)
        for branch_name in branch_data:
            print(branch_name)

        print('\nThe number of branches is {} .'.format(len(branch_data)))
        cli = input('input your option:')

input('logout')
exit()