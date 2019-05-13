#!/usr/bin/env python 

# import required classes
from PIL import Image, ImageDraw, ImageFont
from imgurpython import ImgurClient

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


def CreateCard(text):
  textlist=text.strip().split(',')
  minutes = textlist[1]
  family = textlist[2]
  person = textlist[3]

  # create Image object with the input image
  image = Image.open('./禱告手.jpg')

  # initialise the drawing context with
  # the image object as background
  draw = ImageDraw.Draw(image)

  # create font object with the font file and specify
  # desired size
  #font = ImageFont.truetype(size=14)
  font = ImageFont.load_default()

  # starting position of the message
  (x, y) = (150, 550)
#  message = "我清楚人每一天的時間有限，\n但因著神愛我，\n就願意每天將%s分鐘分別為聖，\n為%s一家的需要\n和靈命穩定增長代禱。\n願神賜我智慧、愛心和耐心，\n真實愛我的弟兄姐妹。\n\n立約人：%s" % (minutes, family, person)
  message = "我清楚人每一天的時間有限\n但因著神愛我\n就願意每天將%s分鐘分別為聖\n為%s一家的需要\n和靈命穩定增長代禱\n願神賜我智慧、愛心和耐心\n真實愛我的弟兄姐妹\n\n立約人：%s" % (minutes, family, person)
  color = 'rgb(255, 255, 255)' # black color
  # draw the message on the background
 # draw.text((x, y), message, fill=color, font=font)

  font = ImageFont.truetype('微软雅黑粗体.ttf',36)
#  draw.text( (x,y), message,fill=color,font=font)
  draw.multiline_text( (x,y), message,fill=color,font=font, spacing=5, align='center')

  # another characters
  (x, y) = (225, 1000)
  name = ' All Right Reseved®Young Couple Fellowship'
  color = 'rgb(0, 0, 0)' # white color
  font = ImageFont.truetype('微软雅黑粗体.ttf',14)
  draw.multiline_text( (x,y), name,fill=color,font=font, spacing=5, align='center')

  # save the edited image
  image.save('greeting_card.png')
  photo_link = upload_photo('greeting_card.png')
  return photo_link

if __name__ == '__main__':
  print(CreateCard('立約小卡,15,賀凱,荃滿'))
