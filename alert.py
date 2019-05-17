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
  authorlist = ['中央氣象局','桃園市']
  keyword='桃園市'
  count = 1
  for message in data:
    author = message['author']['name']
    summary = message['summary']['#text'].strip()
    strfind = summary.find(keyword)
    if author in authorlist or strfind != -1 :
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
  show_alert(data)
#  show_all(data)
