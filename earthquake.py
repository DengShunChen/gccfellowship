#!/usr/bin/env python 
import urllib.request as ur
from bs4 import BeautifulSoup

def get_url():
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
  url='https://www.cwb.gov.tw/V8/C/E/index.html'
  req = ur.Request(url=url, headers=headers)
  thepage = ur.urlopen(req)
  soup = BeautifulSoup(thepage, "html.parser")
  print(soup.prettify())
 
def get_post():
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
  url='https://www.cwb.gov.tw/V8/C/E/index.html'
  req = ur.Request(url=url, headers=headers)
  thepage = ur.urlopen(req)
  soup = BeautifulSoup(thepage, "html.parser")

  # title 
  string = '基督論壇報 焦點新聞'
  content =  string + '\n'
  content = content + url + '\n'
  content = content + '\n'

  posts = soup.find_all('a',class_="featured-thumbnail")
  for p,post in enumerate(posts):
    if p <= 5:
      href = post.get('href')
      title = post.get('title')
      content = content +  title + '\n'
      content = content +  href + '\n'

  return content 

if __name__ == '__main__':

  print(get_url())
#  print(get_post())
 
