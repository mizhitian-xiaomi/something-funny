import requests
import json

class commits_data(object):
    def __init__(self): 
        self.branch_url = 'https://gitlab.com/api/v4/projects/13020942/repository/branches?private_token=1AMA7UwiNgNKBHpRTVS-&page=1&per_page=50'
        self.commit_url = 'https://gitlab.com/api/v4/projects/13020942/repository/commits?ref_name={}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        self.params = {
            "private_token": "1AMA7UwiNgNKBHpRTVS-",
            "page": "1",
            "per_page": "100"
        }
        branch_all = requests.get(self.branch_url)
        data = json.loads(branch_all.text)
        # print(data)
        
        for branch in data:
            name_list = []
            name = branch['name']
            name_list.append(name)
            # print(name_list)
            # print(len(name_list))
            for i in name_list:
                print('\n', '分支名称 → {}'.format(i))
                commit_url = self.commit_url.format(i)
                # print('分支地址 → ', commit_url)
                
                r = requests.get(commit_url,params=self.params) 

                commit_one = json.loads(r.text)
                # print(commit_one, '\n')
                commit_list = []
                for j in commit_one:
                    commit = {}
                    commit['何时'] = j['created_at']
                    commit['由谁'] = j['author_name']
                    commit_list.append(commit)
                    print('何时 → ', str(commit['何时']),'由谁 → ', str(commit['由谁']))
                
        

if __name__ == '__main__':
    commits_data = commits_data()
#     issues_data.run()





   