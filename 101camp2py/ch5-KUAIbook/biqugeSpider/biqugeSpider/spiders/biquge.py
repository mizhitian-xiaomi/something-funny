# -*- coding: utf-8 -*-
import scrapy.spiders
import time
import tkinter.messagebox
import biqugeSpider.bbk.window as bw

# 请在该目录下运行
# ch5-KUAIbook\biqugeSpider\biqugeSpider
# scrapy crawl biquge

class BiqugeSpider(scrapy.Spider):
    name = 'biquge'
    # 域名搜索范围，规定只能爬取该域名下的网页
    allowed_domains = ['biquge.com.cn']
    # 爬虫从该列表开始
    book_name = None
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }
    flag = True


    def start_requests(self):
        """生成指定书籍的搜索页面
        :return:
        """
        BiqugeSpider.book_name = bw.BOOK
        print(BiqugeSpider.book_name)
        url = 'https://www.biquge.com.cn/search.php?keyword={}'.format(BiqugeSpider.book_name)
        yield scrapy.Request(url=url, callback=self.parse, headers=BiqugeSpider.headers, method='GET')

    def parse(self, response):
        """负责解析搜索页面，获取book_id从而得到指定小说的目录页面
        :param response:
        :return:
        """
        self.book_url = response.xpath('/html/body/div[2]/div/div[2]/h3/a/@href').extract_first()

        if self.book_url is not None:
            item = {}
            # 通过xpath分析小说信息
            name = response.xpath('/html/body/div[2]/div/div[2]/h3/a/span/text()').extract_first()
            if name == BiqugeSpider.book_name:
                item['name'] = '《' + name + '》\n'
                item['author'] = "作者：" + response.xpath(
                    '/html/body/div[2]/div/div[2]/div/p[1]/span[2]/text()').extract_first().replace(' ', ''). \
                    replace('\n', '').replace('\r', '') + '\n'
                item['type'] = "类型：" + response.xpath(
                    '/html/body/div[2]/div/div[2]/div/p[2]/span[2]/text()').extract_first() + '\n'
                item['desc'] = "简介：" + response.xpath(
                    '/html/body/div[2]/div/div[2]/p/text()').extract_first().replace(' ', '') + '\n'

                # 递归解析小说章节网页
                yield scrapy.Request(url=self.book_url, meta={'item': item}, callback=self.parse_chapters,
                                     headers=BiqugeSpider.headers,
                                     method='GET')
            else:
                tkinter.messagebox.showerror('抱歉', '非常抱歉，您需要的小说我们没有找到')

                return False
        else:
            tkinter.messagebox.showerror('抱歉', '非常抱歉，您需要的小说我们没有找到')
            return False

    def parse_chapters(self, response):
        """获得小说每一章的url
        :param response:
        :return:
        """
        item = response.meta['item']
        htmlid_list = response.xpath('//*[@id="list"]/dl/dd/a/@href').extract()
        chapter_list = response.xpath('//*[@id="list"]/dl/dd/a/text()').extract()
        for htmlid, chapter in zip(htmlid_list, chapter_list):
            url = self.book_url + htmlid.split('/')[3]
            time.sleep(0.01)
            if url is not None:
                yield scrapy.Request(url=url, callback=self.parse_content, meta={'item': item},
                                     headers=BiqugeSpider.headers, method='GET')
            else:
                print("该书籍还未更新章节噢....")

    def parse_content(self, response):
        """解析每一章节的内容
        :param response:
        :return:
        """
        item = response.meta['item']
        contents = '-' * 30 + '\n'
        title = response.xpath('//div[@class="bookname"]/h1/text()').extract_first()
        text = response.xpath('//*[@id="content"]/text()').extract()
        for t in text:
            content = t.replace('<br/>', '').replace('<p>', '').replace('</p>', '') + '\n'
            contents += content
        # print(title)
        item['content'] = '-' * 30 + '\n' + title + '\n' + contents
        if BiqugeSpider.flag == True:
            BiqugeSpider.flag = False
            yield item
        # 很捞却有用的处理方法//尬笑...
        else:
            item['author'] = ''
            item['name'] = ''
            item['author'] = ''
            item['type'] = ''
            item['desc'] = ''
            yield item
