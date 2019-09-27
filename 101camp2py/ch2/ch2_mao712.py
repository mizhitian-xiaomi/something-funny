import requests
import json

class issues_data(object):
    def __init__(self):
        self.start_url = 'https://gitlab.com/api/v4/projects/13020942/issues?private_token=CbHKxQNVND-4Ss7rKQSr&per_page=100'
        # self.url = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        self.params = {
            "private_token": "CbHKxQNVND-4Ss7rKQSr",
            "page": "1",
            "per_page": "100"
        }
        print(self.start_url)
        with open('IssueData.csv', 'a') as f:
            f.write('iid, 作者, 评论次数'+'\n')
    
    def get_json(self):
        ret = requests.get(self.start_url, headers=self.headers, params=self.params)
        jsonobj = json.loads(ret.text)
        content_list = []
        for i in jsonobj:
            content = {}
            content['iid'] = i['iid']
            content['作者'] = i['author']['name']
            content['评论次数'] = i['user_notes_count']
            content_list.append(content)
        print(content_list)
        
        return content_list



    def save(self, content_list):
        with open('IssueData.csv', 'a') as f:
            for content in content_list:
                f.write(str(content['iid'])+','+str(content['作者'])+','+str(content['评论次数'])+'\n')
        
    def run(self):
        content_list = self.get_json()
        self.save(content_list)

if __name__ == '__main__':
    issues_data = issues_data()
    issues_data.run()





   