#!/usr/bin/env python 

# import required classes
from PIL import Image, ImageDraw, ImageFont
import json
import random
from tools import Toolbox 

def CreateCard(propose='金句'):
  bkgds_id = random.randint(0,12)
  bkgd = './picture/背景%2.2d.jpg' % (bkgds_id)

  # character color 
  blacklist = [1, 2, 6, 7, 8, 9, 10,  11]
  if bkgds_id in blacklist :
    color = 'rgb(0, 0, 0)' # black color
  else:
    color = 'rgb(255, 255, 255)' # white color

  with open('goldenverse.json', 'r') as f :
    verses = json.load(f)

  # 使用金句 
  verses = verses[propose]

  # random selecte 
  verse_id = random.randint(0,len(verses)-1)

  # create Image object with the input image
  image = Image.open(bkgd)

  # initialise the drawing context with
  # the image object as background
  draw = ImageDraw.Draw(image)

  # create font object with the font file and specify
  # desired size
  font = ImageFont.load_default()

  # starting position of the message
  message = verses[verse_id]['content'] 

#  print(len(message))
  if len(message) <= 18:
    fontsize = 52
    verse_y = 190
    content_x = 75
    content_y = 150
  elif len(message) > 18 and len(message) <= 45 :
    fontsize=43
    verse_y = 220
    content_x = 60
    content_y = 140
  elif len(message) > 45 and len(message) <= 65 :
    fontsize=40
    verse_y = 230
    content_x = 60
    content_y = 130
  else:
    fontsize=38
    verse_y = 260
    content_x = 60
    content_y = 130
 
  (x, y) = (content_x, content_y)
  # draw the message on the background
# font = ImageFont.truetype('微软雅黑粗体.ttf',36)
  font = ImageFont.truetype('./font/HanyiSentyTang.ttf',fontsize)
# font = ImageFont.truetype('./font/SentyGoldenBell.ttf',38)
  draw.multiline_text( (x,y), message,fill=color,font=font, spacing=5, align='left')

  # starting position of the message
  message = verses[verse_id]['verse']
  if len(message) <= 6:
    fontsize = 40
    verse_x = 750
  else:
    fontsize = 34
    verse_x = 650

  (x, y) = (verse_x, verse_y)
# font = ImageFont.truetype('微软雅黑粗体.ttf',36)
  font = ImageFont.truetype('./font/SentySnowMountain.ttf',fontsize)
  draw.multiline_text( (x,y), message,fill=color,font=font, spacing=5, align='right')

  # another characters
  (x, y) = (350, 370)
  name = 'Young Couple Fellowship X Glory Christian Church'

  # character color 
  whitelist = [0, 8, 4, 5, 11, 12]
  if bkgds_id in whitelist :
    color = 'rgb(255, 255, 255)' # white color
  else:
    color = 'rgb(0, 0, 0)' # black color

  fontsize=16
  font = ImageFont.truetype('./font/SentySnowMountain.ttf',fontsize)
#  font = ImageFont.truetype('./font/微软雅黑粗体.ttf',14)
#  font = ImageFont.truetype('./font/SentyGoldenBell.ttf',38)
  draw.multiline_text( (x,y), name,fill=color,font=font, spacing=5, align='center')

  # save the edited image
  image.save('verse_card.png')

  tb = Toolbox()
  photo_link = tb.upload_photo('verse_card.png')
  return photo_link

if __name__ == '__main__':
  print(CreateCard('醫治'))
