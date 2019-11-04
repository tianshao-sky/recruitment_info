import csv

from boss_zhipin import Boss
from zhilian_zhaopin import Zhilian
from lagou_net import Lagou

header = ['职位名','薪资','地点','经验','学历','公司名','详细信息url']
with open('jobs.csv','w',newline='')as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)

boss = Boss()
zhilian = Zhilian()
lagou = Lagou()

print('************开始爬BOSS直聘************')
boss.main()
print('************开始爬智联招聘************')
zhilian.main()
print('************开始爬拉钩网************')
lagou.main()