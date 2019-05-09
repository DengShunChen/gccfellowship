#!/usr/bin/env python 
import urllib.request as ur
from bs4 import BeautifulSoup

def get_url():
  url='https://traditional-odb.org'
  thepage = ur.urlopen(url)
  soup = BeautifulSoup(thepage, "html.parser")
  todayurl = soup.find_all('meta',property="og:url")
  for ogurl in todayurl:
    url = ogurl.get('content')

  return url
 
def get_post():
#  url='https://traditional-odb.org/today/'
#  url='https://traditional-odb.org/2019/05/02/%E6%81%86%E5%88%87%E7%A6%B1%E5%91%8A-2/'
  url = get_url()
  thepage = ur.urlopen(url)
  soup = BeautifulSoup(thepage, "html.parser")

  content = url + '\n'
  # title 
  string = soup.h2.text
  content = content +  string + '\n'

  golden_verse = soup.find_all('div',class_="verse-box")
  for v in golden_verse:
    string = v.text
    content = content +  string + '\n'

  posts = soup.find_all('div',class_="post-content")
  for v in posts:
    string = v.text
    content = content +  string + '\n'

  posts = soup.find_all('p')
  for post in posts:
    if post.text == '你必須登錄書籤':
      break
    else: 
      if post.parent.name == '[document]':
        string = post.text
        content = content +  string.strip() + '\n'
        content = content +  '\n'

#   poem=soup.find_all('div',class_="insight-wrapper")
#   for v in poem:
#     string = v.text
#     print(string)
#     content = content +  string.strip() 

  return content 

if __name__ == '__main__':

#  print(get_url())
  print(get_post())
 
