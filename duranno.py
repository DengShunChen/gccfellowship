#!/usr/bin/env python 
import urllib.request as ur
from bs4 import BeautifulSoup

def get_url():
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
  url='http://www.duranno.tw/livinglife/index.php/daily'
  req = ur.Request(url=url, headers=headers)
  thepage = ur.urlopen(req)
  soup = BeautifulSoup(thepage, "html.parser")
  print(soup.prettify())
 
def get_post():
#  url='https://traditional-odb.org/today/'
#  url='https://traditional-odb.org/2019/05/02/%E6%81%86%E5%88%87%E7%A6%B1%E5%91%8A-2/'
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
  url='http://www.duranno.tw/livinglife/index.php/daily'
  req = ur.Request(url=url, headers=headers)
  thepage = ur.urlopen(req)
  soup = BeautifulSoup(thepage, "html.parser")

  # title 
  string = '活潑的生命 每日經文'
  content =  string + '\n'
  content = content + url + '\n'
  content = content + '\n'

  posts = soup.find_all('div',class_="in_body")
  for p,post in enumerate(posts):
    title = post.text
    content = content +  title + '\n'

  return content 

if __name__ == '__main__':

#  print(get_url())
  print(get_post())
 
