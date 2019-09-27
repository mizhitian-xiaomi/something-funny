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
        # print(data[0]['name'])
        number_branch = len(data)


        x = 0
        name_list = []
        while x < number_branch:
            name = {}
            name = data[x]['name']
            name_list.append(name)
            x += 1
            print(name_list)
            
        y = 0
        m = []
        while y < number_branch:
            i = name_list[y]
            commit_url = self.commit_url.format(i)
            r = requests.get(commit_url,params=self.params)
            commit_one = json.loads(r.text)
            ci = len(commit_one)
            rank_ci = (ci, i)
            y += 1
            m.append(rank_ci)
            print(m)

        rank_m = sorted(m, reverse = True)
        print(rank_m)

        print('top 1 of ci → {}.'.format(rank_m[0]))
        print('top 2 of ci → {}.'.format(rank_m[1]))
        print('top 3 of ci → {}.'.format(rank_m[2]))
        print('top 4 of ci → {}.'.format(rank_m[3]))
        print('top 5 of ci → {}.'.format(rank_m[4]))

        
        
        

if __name__ == '__main__':
    commits_data = commits_data()
#     issues_data.run()





   