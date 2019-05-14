#!/usr/bin/env python 

# import required classes
from PIL import Image, ImageDraw, ImageFont
from imgurpython import ImgurClient
import json
import random

def upload_photo(photo_path):
  client_id = '1abfc96a9fd1cc6'
  client_secret = 'b90e27ab19ee4f3893c4442c2a4a3fba9035f0d0'
  access_token = '0cd8b2fe6740013637b3c1fd62954237540d4529'
  refresh_token = '0811df48b103bbdb19fdaeec1b4f5912bf8e8319'
  client = ImgurClient(client_id, client_secret, access_token, refresh_token)
  album = None # You can also enter an album ID here
  config = {
    'album': album,
  }

  print("Uploading image... ")
  image = client.upload_from_path(photo_path, config=config, anon=False)
  print("Done")    
  return image['link']

def CreateCard():

  verse_id = random.randint(0,49)
  bkgd = './picture/天空.jpg'

  with open('goldenverse.json', 'r') as f :
    verses = json.load(f)
#    print(verses) 
 
  verses = verses['金句']
 
  # create Image object with the input image
  image = Image.open(bkgd)

  # initialise the drawing context with
  # the image object as background
  draw = ImageDraw.Draw(image)

  # create font object with the font file and specify
  # desired size
  #font = ImageFont.truetype(size=14)
  font = ImageFont.load_default()

  # starting position of the message
  (x, y) = (100, 150)
  message = verses[verse_id]['content'] 
  color = 'rgb(255, 255, 255)' # white color
#  color = 'rgb(0, 0, 0)' # black color
  # draw the message on the background
 # draw.text((x, y), message, fill=color, font=font)
# font = ImageFont.truetype('微软雅黑粗体.ttf',36)
# font = ImageFont.truetype('HanyiSenty.ttf',52)
  font = ImageFont.truetype('./font/SentyGoldenBell.ttf',38)
#  draw.text( (x,y), message,fill=color,font=font)
  draw.multiline_text( (x,y), message,fill=color,font=font, spacing=5, align='center')

  # starting position of the message
  (x, y) = (700, 200)
  message = verses[verse_id]['verse']
  color = 'rgb(255, 255, 255)' # white color
#  color = 'rgb(0, 0, 0)' # black color
  # draw the message on the background
 # draw.text((x, y), message, fill=color, font=font)
# font = ImageFont.truetype('微软雅黑粗体.ttf',36)
  font = ImageFont.truetype('./font/SentySnowMountain.ttf',42)
#  draw.text( (x,y), message,fill=color,font=font)
  draw.multiline_text( (x,y), message,fill=color,font=font, spacing=5, align='right')

  # another characters
  (x, y) = (350, 370)
  name = ' All Right Reseved®Young Couple Fellowship'
  color = 'rgb(255, 255, 255)' # white color
  color = 'rgb(0, 0, 0)' # black color
#  font = ImageFont.truetype('SentySnowMountain.ttf',14)
  font = ImageFont.truetype('./font/微软雅黑粗体.ttf',14)
  draw.multiline_text( (x,y), name,fill=color,font=font, spacing=5, align='center')

  # save the edited image
  image.save('verse_card.png')
  photo_link = upload_photo('verse_card.png')
  return photo_link

if __name__ == '__main__':
  print(CreateCard())
