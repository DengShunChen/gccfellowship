#!/usr/bin/env python 
import urllib.request as ur
from bs4 import BeautifulSoup

def get_post():
  url='https://traditional-odb.org/today/'
  thepage = ur.urlopen(url)
  soup = BeautifulSoup(thepage, "html.parser")

  content = ''
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

  print(get_post())
#  print(db.get_all())
 
