#!/usr/bin/env python
from datetime import datetime, timedelta
import json
import urllib.request as ur
import urllib.parse as up
import ssl

# read json file 
def read_json(url):
  ssl._create_default_https_context = ssl._create_unverified_context
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
  req = ur.Request(url=url, headers=headers)
  urldata = ur.urlopen(req)
  data = json.loads(urldata.read())
  return data

def bible(bookname='箴',chap=1, sec=None):
  # prepare url
  book = up.quote(bookname)
  try:
    chap = int(chap)
  except:
    string = '章節設置錯誤-->"%s"' % (chap)
    return string

  if not sec == None:
    url = "https://bible.fhl.net/json/qb.php?chineses=%s&chap=%d&sec=%s" % (book,int(chap),sec)
  else:
    url = "https://bible.fhl.net/json/qb.php?chineses=%s&chap=%d" % (book,int(chap))

  # get data
  data = read_json(url)

  string = ['','']

  n=0
  string[n] = '%s:%d\n' % (bookname,int(chap))

  if data['status'] == "success":
    for r in data['record']:  
      verse = '%d.%s' % (r['sec'],r['bible_text'])
      if len(string[n]) > 1950:
        string[n+1] = string[n+1] + verse + '\n'
      else: 
        string[n] = string[n] + verse + '\n'

  return string


if __name__ == '__main__':
  print(bible('路','12','22-34'))
#  print(show_all(data))
