#!/usr/bin/env python 

# import required classes
from PIL import Image, ImageDraw, ImageFont


def CreateCard(text):
  textlist=text.strip().split(',')
  minutes = textlist[1]
  family = textlist[2]
  person = textlist[3]

  # create Image object with the input image
  image = Image.open('./background2.jpg')

  # initialise the drawing context with
  # the image object as background
  draw = ImageDraw.Draw(image)

  # create font object with the font file and specify
  # desired size
  #font = ImageFont.truetype(size=14)
  font = ImageFont.load_default()

  # starting position of the message
  (x, y) = (10, 10)
  message = "我清楚人每一天的時間有限，但因著神愛我，"

  color = 'rgb(0, 0, 0)' # black color
  # draw the message on the background
 # draw.text((x, y), message, fill=color, font=font)

  font = ImageFont.truetype('simsun.ttc',24)
  draw.text( (0,50), u'你好,世界!',(0,0,0),font=font)
  draw.text((0,60),unicode('你好','utf-8'),(0,0,0),font=font) 


  # another characters
# (x, y) = (150, 150)
# name = 'Vinay'
# color = 'rgb(255, 255, 255)' # white color
# draw.text((x, y), name, fill=color, font=font)

  # save the edited image
  image.save('greeting_card.png')

if __name__ == '__main__':
  CreateCard('立約小卡,15,禎祐,登舜')
