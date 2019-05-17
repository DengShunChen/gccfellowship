#!/usr/bin/env python
import json
import urllib.request as ur

# read json file 
def read_json(url):
  urldata = ur.urlopen(url)
  data = json.loads(urldata.read())
  return data

def show_alert(data):
  string = '[警特報]\n'
  authorlist = ['中央氣象局']
  keywordlist=['桃園市','台北市','新北市','新竹市','新竹縣']
  count = 1
  for message in data:
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
  return string

def show_all(data):
  string = '[警特報]\n'
  count = 1
  for message in data:
    author = message['author']['name']
    summary = message['summary']['#text'].strip()
    string = string + '%2d. %s: \n%s \n\n' % (count,author,summary)
    count+=1
  return string


if __name__ == '__main__':
  url = 'https://alerts.ncdr.nat.gov.tw/JSONAtomFeeds.ashx'
  data = read_json(url)['entry']
  print(show_alert(data))
#  print(show_all(data))
