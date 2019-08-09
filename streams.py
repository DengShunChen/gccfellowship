#!/usr/bin/env python 
import urllib.request as ur
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def get_url():
  GMT_plus_8 = timedelta(hours=8)
  now = datetime.utcnow() + GMT_plus_8
#  now = datetime.today()

  month = now.strftime("%m")
  day = now.strftime("%d")  
  url='https://www.fhl.net/stream/%d/%2.2d%2.2d.htm' % (int(month),int(month),int(day))

# thepage = ur.urlopen(url)
# soup = BeautifulSoup(thepage, "html.parser")
# todayurl = soup.find_all('meta',property="og:url")
# for ogurl in todayurl:
#   url = ogurl.get('content')

  return url
 
def get_post():
#  url='https://traditional-odb.org/today/'
#  url='https://traditional-odb.org/2019/05/02/%E6%81%86%E5%88%87%E7%A6%B1%E5%91%8A-2/'

  url = get_url()

  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
  req = ur.Request(url=url, headers=headers)
  thepage = ur.urlopen(req)
  soup = BeautifulSoup(thepage, "html.parser")

  content = url + '\n'
  # title 
#  string = soup.title.text
#  content = content +  string + '\n'
  golden_verse = soup.find_all('font')
  string = golden_verse[0].text.rstrip()
  content = content +  string + '\n'
  string = golden_verse[1].text.rstrip()
  content = content +  string + '\n'

  golden_verse = soup.find_all('p')
  string = golden_verse[1].text.rstrip()
  content = content +  string + '\n'

# for v in golden_verse:
#   string = v.text
#   content = content +  string + '\n'

  return content 

if __name__ == '__main__':

  print(get_url())
  print(get_post())
 
