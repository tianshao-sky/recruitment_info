import csv

import requests
from fake_useragent import UserAgent
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Boss():
    def __init__(self):
        self.headers = {
            'User-Agent': str(UserAgent().random),
        }
        self.proxies = {
            "http": "http://39.108.90.252:8000"
        }
        self.base_url = 'https://www.zhipin.com/c101210100/?query=python&page='
        self.info = []

    def get_cookies(self,page):
        # 防止检测
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get('https://www.zhipin.com/c101210100/?query=python&page='+ str(page))
        c = driver.get_cookies()
        self.cookies = {}
        # 获取cookie中的name和value,转化成requests可以使用的形式
        for cookie in c:
            self.cookies[cookie['name']] = cookie['value']
        driver.close()

    def send_request(self,page):
        response = requests.get(self.base_url+str(page),headers=self.headers, proxies=self.proxies,cookies=self.cookies)
        html = response.content.decode('utf-8')
        return html

    def parse(self,html):
        xml = etree.HTML(html)
        nodes = xml.xpath('//div[@class="job-list"]/ul/li')

        for node in nodes:
            item = {}
            # 职位名
            item['name'] = node.xpath('.//div[@class="info-primary"]/h3/a/div[1]/text()')[0]
            # 薪资
            item['salary'] = node.xpath('.//div[@class="info-primary"]/h3/a/span/text()')[0]
            # 地点
            item['place'] = node.xpath('.//div[@class="info-primary"]/p/text()')[0]
            # 经验
            item['experience'] = node.xpath('.//div[@class="info-primary"]/p/text()')[-2]
            # 学历
            item['degree'] = node.xpath('.//div[@class="info-primary"]/p/text()')[-1]
            # 公司名
            item['company'] = node.xpath('.//div[@class="company-text"]/h3/a/text()')[0]
            # 详细信息url
            item['next_url'] ='www.zhipin.com'+node.xpath('.//div[@class="info-primary"]/h3/a/@href')[0]
            self.info.append(item)

        return xml.xpath('//div[@class="page"]/a[last()]/@class')[0]

    def save(self):
        data = [info.values() for info in self.info]
        with open('jobs.csv', 'a+',newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(data)


    def main(self):
        page = 1
        print('------获取可用cookies中------')
        self.get_cookies(page)
        while True:
            try:
                html = self.send_request(page=page)
                flag = self.parse(html)
                print(str(page) + '----------OK')
                page += 1
                if flag != 'next':
                    break
            except IndexError:
                # 重新获得可用cookies
                print('------获取可用cookies中------')
                self.get_cookies(page)
        self.save()
