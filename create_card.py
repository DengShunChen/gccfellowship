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
  (x, y) = (150, 150)
  message = "我清楚人每一天的時間有限，但因著神愛我，\n\n就願意每天將____(幾分鐘)分別為聖，\n\n為XXX一家的需要和靈命穩定增長代禱。\n\n願神賜我智慧、愛心和耐心，真實愛我的弟兄姐妹。\n\n立約人：XXX"
  color = 'rgb(0, 0, 0)' # black color
  # draw the message on the background
 # draw.text((x, y), message, fill=color, font=font)

  font = ImageFont.truetype('simsun.ttc',72)
  font = ImageFont.truetype('TPOP03B.TTF',72)
  draw.text( (x,y), message,fill=color,font=font)


  # another characters
# (x, y) = (150, 150)
# name = 'Vinay'
# color = 'rgb(255, 255, 255)' # white color
# draw.text((x, y), name, fill=color, font=font)

  # save the edited image
  image.save('greeting_card.png')

if __name__ == '__main__':
  CreateCard('立約小卡,15,禎祐,登舜')
