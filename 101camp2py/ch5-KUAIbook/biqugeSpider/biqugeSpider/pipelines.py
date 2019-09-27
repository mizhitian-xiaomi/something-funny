# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import time
import tkinter.filedialog
import os


# 存储信息到本地使用的类

class BiqugespiderPipeline(object):
    flag = True

    def open_spider(self, spider):
        """
        :param spider:
        :return:
        """
        now = tkinter.filedialog.asksaveasfilename()
        self.file = open(now, 'w', encoding='utf-8')
        # self.file = open('book/{}.txt'.format(now), 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()
        if BiqugespiderPipeline.flag is False:
            print('$$$\n'+self.file.name+'\n$$$')
            os.remove(self.file.name)
        # else:
        #     # 返回文件名
        #     print(type(a))

    def process_item(self, item, spider):
        try:
            res = dict(item)
            name = res['name']
            author = res['author']
            type = res['type']
            desc = res['desc']
            self.file.write(author)
            self.file.write(type)
            self.file.write(desc)

            content = res['content']
            self.file.write(content + '\n')
            if len(content) < 1:
                BiqugespiderPipeline.flag = False
        except Exception as e:
            print(e)
            print("存储失败！")
