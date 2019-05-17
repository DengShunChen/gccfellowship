#!/usr/bin/env python
from tools import Toolbox

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

