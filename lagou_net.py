import csv
import time

import requests
from fake_useragent import UserAgent


class Lagou():
    def __init__(self):
        self.headers = {
            'User-Agent': str(UserAgent().random),
            'Referer': 'https://www.lagou.com/jobs/list_Python/p-city_6'
        }
        self.proxies = {"http": "http://121.232.194.196:9000"}
        self.info = []

    def get_cookies(self):
        response = requests.get('https://www.lagou.com/jobs/list_python/p-city_6', headers=self.headers,proxies=self.proxies)
        self.cookies = response.cookies

    def send_request(self,data):
        response = requests.post('https://www.lagou.com/jobs/positionAjax.json?city='+'杭州', data=data,cookies = self.cookies ,headers=self.headers, proxies=self.proxies)
        json_ = response.json()
        return json_

    def parse(self,json_):
        nodes = json_.get('content').get('positionResult').get('result')
        if nodes == []:
            # 结束标志
            return 'finish'
        for node in nodes:
            item = {}
            # 职位名
            item['name'] = node.get('positionName').replace('\u2f2f','工')
            # 薪资
            item['salary'] = node.get('salary')
            # 地点
            if node.get('district'):
                item['place'] = node.get('city') +' '+ node.get('district')
            else:
                item['place'] = node.get('city')
            # 经验
            item['experience'] = node.get('workYear')
            # 学历
            item['degree'] = node.get('education')
            # 公司名
            item['company'] = node.get('companyFullName')
            # 详细信息url
            item['next_url'] = 'www.lagou.com/jobs/'+ str(node.get('positionId'))+'.html'
            self.info.append(item)

    def save(self):
        data = [info.values() for info in self.info]
        with open('jobs.csv', 'a+', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(data)

    def main(self):
        page = 1
        print('------获取可以cookies------')
        self.get_cookies()
        while True:
            try :
                data = {
                    'first': 'true',
                    'pn': page,
                    'kd': 'python',
                    'sid': '90688bed69e54750becf9c99e0c5a90b'
                }
                json_ = self.send_request(data)
                flag = self.parse(json_)
                print(str(page) + '------OK')
                page += 1
                if flag == 'finish':
                    break
            except AttributeError:
                # 重新获取可用cookies
                print('------获取可用cookies中------')
                self.get_cookies()
                time.sleep(10)
        self.save()

