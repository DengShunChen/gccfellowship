#!/usr/bin/env python
from datetime import datetime, timedelta
import json
import urllib.request as ur

# read json file 
def read_json(url):
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
  req = ur.Request(url=url, headers=headers)
  urldata = ur.urlopen(req)
  data = json.loads(urldata.read())
  return data

def show_alert(data):
  GMT_plus_8 = timedelta(hours=8)
  string = '[北北桃竹地區 警特報'+ (datetime.utcnow()+GMT_plus_8).strftime("%Y/%m/%d %H:%M:%S") +']\n'
  authorlist = ['中央氣象局']
  keywordlist=['桃園市','台北市','新北市','新竹市','新竹縣','基隆市','宜蘭縣']
  count = 1
  if type(data) is dict:
    author = data['author']['name']
    summary = data['summary']['#text'].strip()

    stringfind = False
    for keyword in keywordlist:
      if summary.find(keyword) != -1:
        stringfind = True
        break
    authorfind = author in authorlist
    if authorfind or stringfind :
      string = string + '%2d. %s: \n%s \n\n' % (count,author,summary)
      count+=1
  else: 
    for message in data:
      print('message :',message)
      author = message['author']['name']
      summary = message['summary']['#text'].strip()

      stringfind = False
      for keyword in keywordlist:
        if summary.find(keyword) != -1:
          stringfind = True
          break
      authorfind = author in authorlist
      if authorfind or stringfind :
        string = string + '%2d. %s: \n%s \n\n' % (count,author,summary)
        count+=1
  if count == 1:
     string = string + '您好！目前沒有警特報訊息！'
  return string

def show_all(data):
  string = '[警特報]\n'
  count = 1
  if type(data) is dict:
    author = data['author']['name']
    summary = data['summary']['#text'].strip()
    string = string + '%2d. %s: \n%s \n\n' % (count,author,summary)
  else:
    for message in data:
      print('message :',message)
      author = message['author']['name']
      summary = message['summary']['#text'].strip()
      string = string + '%2d. %s: \n%s \n\n' % (count,author,summary)
      count+=1
  return string


if __name__ == '__main__':
  url = 'https://alerts.ncdr.nat.gov.tw/JSONAtomFeeds.ashx'
  data = read_json(url)['entry']
#  print(show_alert(data))
  print(show_all(data))
