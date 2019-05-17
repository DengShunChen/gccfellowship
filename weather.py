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

def satellite():
  url = 'https://www.cwb.gov.tw/Data/satellite/LCC_VIS_TRGB_1000/LCC_VIS_TRGB_1000.jpg'
  tb.download_image(url,'./satellite.jpg')
  url = tb.upload_photo('./satellite.jpg')
  return url

def rain():
  url = 'https://www.cwb.gov.tw/Data/rainfall/QZJ.jpg'
  tb.download_image(url,'./rain.jpg')
  url = tb.upload_photo('./rain.jpg')
  return url
