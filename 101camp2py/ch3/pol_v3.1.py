import requests
import json
import os
import re

'''
url禁止！大写 和 -

'''


class Gitlab(object):
    def __init__(self):
        """ 初始化一些url\headers\params

        per_page 自行修改，gitlab默认是20
        因为目前的代码还未优化，耗时太长，为了快点看到结果我就只让他显示了10条issue结果 params_i

        private_token 可以修改成自己生成的

        """
        self._branch_url = 'https://gitlab.com/api/v4/projects/13020942/repository/branches?'

        self._issue_url = 'https://gitlab.com/api/v4/projects/13020942/issues?'

        self._note_url = 'https://gitlab.com/api/v4/projects/13020942/issues/{}/notes'

        self._commit_url = 'https://gitlab.com/api/v4/projects/13020942/repository/commits?ref_name={}'

        self._commit_comments_url = "https://gitlab.com/api/v4/projects/13020942/repository/commits/{}/comments"


        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/75.0.3770.142 Safari/537.36"
        }

        # branch 默认一页是20条,max=100，目前所有的是39
        self.params = {
            "private_token": "1AMA7UwiNgNKBHpRTVS-",
            "page": "1",
            "per_page": "100"
        }
        # issue
        self.params_i = {
            "private_token": "1AMA7UwiNgNKBHpRTVS-",
            "page": "1",
            "per_page": "10"
        }

        with open("issue.json", "a") as fp:
            fp.write("iid, author, url, note " + "\n")


def get_branch(self):
    """ 获取task仓库下分支

    :param self:
    :return: name_list 分支名字集合
    """
    brh_ret = requests.get(self._branch_url, headers=self.headers, params=self.params)
    data = brh_ret.json()
    name_list = []
    for branch in data:
        name = branch['name']
        if name != 'master':
            name_list.append(name)
    return name_list


def get_issue(self):
    """ 获取issue信息
    编号：iid - iid
    标题：title - title
    作者：author - author-name
    url： url - web_url
    评论: note - get_issnote(self, content['iid'])

    :param self:
    :return: content_list 每个issue的dict的集合
    """
    iss_ret = requests.get(self._issue_url, headers=self.headers, params=self.params_i)
    # 把json格式字符串转换成python对象
    jsonobj = json.loads(iss_ret.text)
    content_list = []

    for obj in jsonobj:
        content = {}
        content['iid'] = obj['iid']
        content['title'] = obj['title']
        content['author'] = obj['author']['name']
        content['url'] = obj['web_url']
        content['note'] = get_issnote(self, content['iid'])
        content_list.append(content)

    self.iss_len = len(content_list)

    save(content_list)

    return content_list


def get_issnote(self, iid):
    """ 获取issue下评论回复的数量

    :param self:
    :param iid:
    :return: len(jsonobj)
    """
    url = self._note_url.format(iid)
    ret = requests.get(url, headers=self.headers, params=self.params_i)
    jsonobj = json.loads(ret.text)
    return len(jsonobj)


def get_commit(self, branch):
    """ 获取指定的commit日志
    日期：        date - committed_date
    提交者：      committer - committer_name
    提交者邮件：  email - committer_email
    标题：        title - title
    讨论内容的id: cid - parent_ids(自己定义的意义)

    :param self:
    :param branch:
    :return:
    """

    url = self._commit_url.format(branch)
    ret = requests.get(url, headers=self.headers, params=self.params)
    jsonobj = json.loads(ret.text)
    # 通过观察json文件，我们需要用list来存储一系列数据
    content_list = []

# 获取指定branch下的数据
    for obj in jsonobj:
        # 用一个字典来存我们所需的数据
        content = {}
        content["date"] = obj["committed_date"]
        content["committer"] = obj["committer_name"]
        content["email"] = obj["committer_email"]
        content["title"] = obj["title"]
        content["cid"] = obj["parent_ids"]
        content_list.append(content)

    return content_list


def save(content_list):
    """ 保存issue信息到本地

    :param content_list:
    :return:
    """
    with open('issue.csv', 'a') as fp:
        for content in content_list:
            fp.write(str(content['iid']) + ' , ' + content['author'] + ' , ' + content['url'] + '\n')


def iss_print(self):
    """ 输出issue信息

    :param self:
    :return:
    """
    data_list = get_issue(self)
    for data in data_list:
        print('[issue#{}] had notes → {} .'.format(data['iid'], data['note']))
        print('[title] {}'.format(data['title']))
        print('[author] {}'.format(data['author']))
        print('[url] {}'.format(data['url']))
        print()

    print('\nThe number of issues is {} .'.format(len(data_list)))
    print()


def brh_print(self):
    """ 输出branch信息

    :param self:
    :return:
    """

    data_list = get_branch(self)
    for data in data_list:
        print(data)
    print('\nThe number of branches is {} .'.format(len(data_list)))
    print()


def comt_print(self, branch):
    """ 输出 选定分支的commit日志 及其 讨论信息
    时间：date - created_at
    作者：author - author-name
    讨论：note - note

    :param self:
    :param branch:
    :return:
    """
    # 指定分支查询commit日志
    # data_list: commit日志列表
    data_list = get_commit(self, branch)
    for data in data_list:
        # content_list: commit下所有讨论的集合
        content_list = []
        # 遍历commit日志里某一条记录的所有的parent_id
        for id in data["cid"]:
            # 获取讨论的url
            url = self._commit_comments_url.format(id)
            ret = requests.get(url, params=self.params)
            jsonobj = json.loads(ret.text)
            # 遍历jsonobj中的每一项提取所需数据
            for obj in jsonobj:
                content = {}
                content["date"] = obj["created_at"]
                content["author"] = obj["author"]["name"]
                content["note"] = obj["note"]
                content_list.append(content)
            # 先输出本项commit记录的信息
            print("Author: {} <{}>".format(data["committer"], data["email"]))
            print("Date:   {}".format(data["date"]))
            print()
            print(data["title"].center(50))
            print()
            # 判断该记录是否存在comment数据
            if len(content_list) == 0:
                print()
                continue
            # 再输出本项commit下的comment数据
            print("-" * 15 + "the comments of commit" + "-" * 15)
            for content in content_list:
                print("[{}]: {}".format(content["author"], content["note"]))
                print("at {}".format(content["date"]).rjust(80))
            print()


def run(self):
    """ 运行pol及显示

    :param self:
    :return:
    """
    cli = input('[101camp] input your option: ')
    while cli != 'exit':

        if cli == 'ris branch':
            brh_print(self)
            print()
            cli = input('[101camp] input your option: ')
        elif cli == 'ris issue':
            iss_print(self)
            os.remove('issue.csv')
            print()
            cli = input('[101camp] input your option: ')
        elif cli == 'ris --help':
            print("---------------Available Input--------------")
            print("branch    →   获取task仓库下所有分支")
            print("issue     →   issue活性扫描")
            print("commit     →   获取master的提交日志")
            print("commit <branchname> \n"
                  "           →   获取branchname的提交日志")
            print()
            print()
            cli = input('[101camp] input your option: ')
        # 不带branchname直接输出master下的信息
        elif cli == 'ris commit':
            ask = "master"
            comt_print(gitlab, ask)
            print()
            cli = input('[101camp] input your option: ')
        # 匹配 ris commit branchname
        elif re.match(r'^ris\scommit\s(.*)$', cli):
            m = re.match(r'^ris\scommit\s(.*)$', cli)
            ask = m.group(1)
            comt_print(self, ask)
            # print('\nThe number of commits is {} .'.format(len()))
            cli = input('[101camp] input your option: ')
        else:
            print('SyntaxError: invalid syntax\n')
            print("---------------Available Input--------------")
            print("branch     →   获取task仓库下所有分支")
            print("issue      →   issue活性扫描")
            print("commit     →   获取master的提交日志")
            print("commit <branchname> \n"
                  "           →   获取branchname的提交日志")
            print()
            print()
            cli = input('[101camp] input your option: ')

    input('logout')


if __name__ == '__main__':
    gitlab = Gitlab()
    run(gitlab)
