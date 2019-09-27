import requests as req
from bs4 import BeautifulSoup
import re
import time
import random

"""
还有很多地方没有完善
目前是”很脆弱的“代码
"""

class Biquge(object):

    def __init__(self):
        self.origin_url = 'https://www.biquge.com.cn/book/{}/'
        self.search_url = 'https://www.biquge.com.cn/search.php?keyword='
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }
        self.book_name = None
        self.book_author = None
        self.book_desc = None

    def search(self):
        """搜索功能 unfinished
        :return:
        """
        url = self.search_url + self.book_name
        res = req.request(url=url, headers=self.headers, method='GET')
        soup = BeautifulSoup(res.content, 'html.parser')

        # 找出小说ID
        a_tag = soup.find('a', attrs={"cpos": "title"})
        link = a_tag.get('href')
        self.book_id = link.split('/')[4]

        # 找出书本描述
        p_tag = soup.find("p", attrs={"class": "result-game-item-desc"})
        self.book_desc = p_tag.string

    def get_chapter(self):
        """获取指定书籍章节url
        :return:
        """
        self.search()
        url = self.origin_url.format(self.book_id)
        res = req.request(url=url, headers=self.headers, method='GET')
        soup = BeautifulSoup(res.content, 'html.parser')

        # 找出作者信息
        div_tag = soup.find("div", attrs={"id": "info"})
        self.book_author = div_tag.p.string

        # 想用dict直接存，但是dict保证不了顺序
        self.chapter_names = []
        self.chapter_urls = []

        # 解析html代码，找出<a>标签
        for ddlist in soup.find_all('dd'):
            a = ddlist.find('a')
            link = a.get('href')
            chapter_id = link.split('/')[3]
            url = self.origin_url.format(self.book_id) + chapter_id
            name = a.string
            self.chapter_names.append(name)
            self.chapter_urls.append(url)

    def get_content(self):
        """获取每个章节的内容
        :return:
        """

        self.chapter_content = []

        # 分析html，获取章节内容
        for page in range(len(self.chapter_names)):
            # 暂停随机时间
            time.sleep(random.random() * 10)
            url = self.chapter_urls[page]
            res = req.request(url=url, headers=self.headers, method='GET')
            soup = BeautifulSoup(res.text.encode('utf-8'), "html.parser")
            div_tag = soup.find('div', attrs={"id": "content"})
            texts = div_tag.strings
            content = ''
            for text in texts:
                content += text.replace('<br/>', '').replace(' ', '').replace('<p>', '').replace('</p>', '')
            self.chapter_content.append(content)
            # print(content)

    def save_as_txt(self):
        """保存为.txt文件
        :return:
        """
        path = "D:/programFiles/101.camp/ch5/data/{}.txt".format(self.book_name)
        with open(path, 'w', encoding='utf-8') as fw:
            fw.write("《{}》\n".format(self.book_name))
            fw.write(self.book_author + "\n")
            fw.write(self.book_desc + "\n" * 2)
            for page in range(len(self.chapter_names)):
                fw.write("-" * 30 + "\n" + self.chapter_names[page] + "\n" * 2)
                fw.write(self.chapter_content[page] + "\n")


if __name__ == '__main__':
    bqg = Biquge()
    bqg.book_name = input("请输入您需要的小说：")
    bqg.get_chapter()
    bqg.get_content()
    bqg.save_as_txt()
