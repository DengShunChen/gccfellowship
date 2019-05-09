#!/usr/bin/env python 
import urllib.request as ur
from bs4 import BeautifulSoup

class dailybread(object):
  def __init__(self,url='https://traditional-odb.org/today/'):    
    print(url)
    self.url = url

  def reflash(self):
    self.thepage = ur.urlopen(self.url)
    self.soup = BeautifulSoup(self.thepage, "html.parser")

  def get_title(self):
    self.reflash()
    return self.soup.title.text

  def get_all(self): 
    self.reflash()
    return self.soup.prettify()

  def get_post(self):
    # reloading the webpage
    self.reflash()

    content = ''
    # title 
    string = self.soup.h2.text
    content = content +  string + '\n'

    golden_verse = self.soup.find_all('div',class_="verse-box")
    for v in golden_verse:
      string = v.text
      content = content +  string + '\n'

    posts = self.soup.find_all('div',class_="post-content")
    for v in posts:
      string = v.text
      content = content +  string + '\n'

    posts = self.soup.find_all('p')
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
  url='https://traditional-odb.org/today/'
  db = dailybread()

  print(db.get_post())
#  print(db.get_all())
 
