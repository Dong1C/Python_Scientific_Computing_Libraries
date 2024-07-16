# 1.载入爬虫需要的模块
import csv
import os
import requests
from bs4 import BeautifulSoup as bs

__getAbsPath = lambda s: os.path.join(os.path.dirname(__file__), s)
url = "https://pvp.qq.com/web201605/herolist.shtml"
# 2.伪装请求头
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Connection": "Keep-alive",
}
resp = requests.get(url, headers=header)
print(resp.text)

# 3.解决乱码问题
resp.encoding = "utf-8"
# 转soup并找出英雄ul标签
soup = bs(resp.text, "html.parser")
ul = soup.find("ul", class_="herolist")

# 4.找出英雄名称，图片url及链接地址
lis = ul.find_all("li")
list_hero = []
print(f"lis length:{len(lis)}")

for li in lis:
    t_img = li.find("img")
    name = t_img.get("alt")
    jpg = "http:" + t_img.get("src")
    hre = "http://pvp.qq.com/web201605/" + li.find("a").get("href")
    list_hero.append((name, jpg, hre))
    
# print(list_hero)
# print(len(list_hero))

# 5.保存爬取的英雄信息到csv文件中
with open(__getAbsPath("hero.csv"), "w", encoding="GBK", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["英雄名称", "英雄头像", "详细链接"])
    wr.writerows(list_hero)
