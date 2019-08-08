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
  print(string)
  content =  content + string[2].strip() + '\n'
  index = string.index('  ★\xa0今天的主題')
  content =  content + string[index].strip() + '\n'
  content =  content + string[index+2].strip() + '\n\n'

  index = string.index('  ★\xa0經文範圍')
  content =  content + string[index].strip() + '\n'
  content =  content + string[index+2].strip() + '\n\n'

  index = string.index('  ★\xa0經文摘要')
  content =  content + string[index].strip() + '\n'
  content =  content + string[index+2].strip() + '\n\n'

  content =  content + string[index+5].strip() + '\n'
  content =  content + string[index+12].strip().split('"')[1] + '\n\n'

  index = string.index('  ★\xa0全心禱告')
  content =  content + string[index].strip() + '\n'
  content =  content + string[index+2].strip() + '\n\n'

  index = string.index('  ★\xa0全年讀經')
  content =  content + string[index].strip() + '\n'
  content =  content + string[index+1].strip() + '\n'


  return content 

if __name__ == '__main__':

#  print(get_url())
  print(get_post())
 
