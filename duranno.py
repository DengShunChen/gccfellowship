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
  content = '活潑的生命 每日經文\n'
  content = content + url + '\n\n'

  posts = soup.find_all('div', class_="in_body")
  string = posts[0].text.split('\n')

  content =  content + string[2].strip() + '\n'
  content =  content + string[15].strip() + '\n'
  content =  content + string[17].strip() + '\n\n'
  content =  content + string[19].strip() + '\n'
  content =  content + string[21].strip() + '\n\n'
  content =  content + string[24].strip() + '\n'
  content =  content + string[26].strip() + '\n\n'
  content =  content + string[29].strip() + '\n'
  content =  content + string[36].strip().split('"')[1] + '\n\n'
  content =  content + string[57].strip() + '\n'
  content =  content + string[59].strip() + '\n\n'
  content =  content + string[61].strip() + '\n'
  content =  content + string[62].strip() + '\n'


  return content 

if __name__ == '__main__':

#  print(get_url())
  print(get_post())
 
