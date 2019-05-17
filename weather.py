#!/usr/bin/env python
from tools import Toolbox

tb = Toolbox()
def radar():
  url = 'https://www.cwb.gov.tw/Data/radar/CV1_TW_1000.png'
  tb.download_image(url,'./radar.png')
  url = tb.upload_photo('./radar.png')
  return url

def temp():
  url = 'https://www.cwb.gov.tw/Data/temperature/temp.jpg'
  tb.download_image(url,'./temp.jpg')
  url = tb.upload_photo('./temp.jpg')
  return url

def satellite(parea = '東亞',pchan = '色調強化'): 
  area = {'全景':['FDK','2750'],'東亞':['LCC','2750'], '台灣':['TWI','800']}
  chan = {'可見光':'VIS_Gray','彩色':'IR1_CR','色調強化':'IR1_MB','黑白':'IR1_Gray','真實色':'VIS_TRGB'}   

  if parea == '台灣' and pchan == '可見光':
    size = 1350
  elif parea == '台灣' and pchan == '真實色':
    size = '1375'
  else:
    size = area[parea][1]

  filename = '%s_%s_%s' % (area[parea][0],chan[pchan],size)
  url = 'https://www.cwb.gov.tw/Data/satellite/%s/%s.jpg' % (filename,filename)
  print(url)

  tb.download_image(url,'./satellite.jpg')
  url = tb.upload_photo('./satellite.jpg')
  return url

def rain():
  url = 'https://www.cwb.gov.tw/Data/rainfall/QZJ.jpg'
  tb.download_image(url,'./rain.jpg')
  url = tb.upload_photo('./rain.jpg')
  return url

if __name__ == '__main__':
  print(satellite())
