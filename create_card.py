#!/usr/bin/env python 

# import required classes
from PIL import Image, ImageDraw, ImageFont
from tools import Toolbox

def show():
  string=''
  string = string + '為幫助團契弟兄姊妹能『凡事謝恩，不住禱告』特別製作“立約小卡”產生器，產生後可以將其放在醒目的地方！' + '\n'
  string = string + '\n'
  string = string + '預設禱詞：' + '\n'
  message = '我清楚人每一天的時間有限，但因著神愛我，就願意每天將____分鐘分別為聖，為_______一家的需要和靈命穩定增長代禱。願神賜我智慧、愛心和耐心，真實愛我的弟兄姐妹。\n\n立約人：________ \n'
  string = string + message + '\n'
  string = string + '\n'
  string = string + '請把"喜樂家庭團契小幫手"加入好友，然後輸入______的內容"' + '\n'
  string = string + '例如輸入：' + '\n'
  string = string + '立約小卡,20,逸農/征祐/瑞琴/亞嫺,荃滿' + '\n'

  return string

def CreateCard(text):
  textlist=text.strip().split(',')
  minutes = textlist[1]
  family = textlist[2]
  person = textlist[3]

  # create Image object with the input image
  image = Image.open('./picture/禱告手.jpg')

  # initialise the drawing context with
  # the image object as background
  draw = ImageDraw.Draw(image)

  # create font object with the font file and specify
  # desired size
  #font = ImageFont.truetype(size=14)
  font = ImageFont.load_default()

  # starting position of the message
  (x, y) = (50, 530)
#  message = "我清楚人每一天的時間有限，\n但因著神愛我，\n就願意每天將%s分鐘分別為聖，\n為%s一家的需要\n和靈命穩定增長代禱。\n願神賜我智慧、愛心和耐心，\n真實愛我的弟兄姐妹。\n\n立約人：%s" % (minutes, family, person)
  message = "         我清楚人每一天的時間有限         \n但因著神愛我\n就願意每天將%s分鐘分別為聖\n為%s一家的需要\n和靈命穩定增長代禱\n願神賜我智慧、愛心和耐心\n真實愛我的弟兄姐妹" % (minutes, family)
  color = 'rgb(255, 255, 255)' # black color
  # draw the message on the background
 # draw.text((x, y), message, fill=color, font=font)
# font = ImageFont.truetype('微软雅黑粗体.ttf',36)
# font = ImageFont.truetype('HanyiSenty.ttf',52)
  font = ImageFont.truetype('./font/SentyGoldenBell.ttf',36)
#  draw.text( (x,y), message,fill=color,font=font)
  draw.multiline_text( (x,y), message,fill=color,font=font, spacing=5, align='center')

  # starting position of the message
  (x, y) = (420, 905)
  message = "立約人：%s" % (person)
  color = 'rgb(255, 255, 255)' # black color
  # draw the message on the background
 # draw.text((x, y), message, fill=color, font=font)
# font = ImageFont.truetype('微软雅黑粗体.ttf',36)
  font = ImageFont.truetype('./font/SentySnowMountain.ttf',42)
#  draw.text( (x,y), message,fill=color,font=font)
  draw.multiline_text( (x,y), message,fill=color,font=font, spacing=5, align='right')

  # another characters
  (x, y) = (240, 1000)
  name = ' All Right Reseved®Young Couple Fellowship'
  color = 'rgb(0, 0, 0)' # white color
#  font = ImageFont.truetype('SentySnowMountain.ttf',14)
  font = ImageFont.truetype('./font/微软雅黑粗体.ttf',14)
  draw.multiline_text( (x,y), name,fill=color,font=font, spacing=5, align='center')

  # save the edited image
  image.save('greeting_card.png')
  tb = Toolbox()
  photo_link = tb.upload_photo('greeting_card.png')
  return photo_link

if __name__ == '__main__':
  print(CreateCard('立約小卡,15,賀凱/柴傳道,荃滿'))
#  print(show())
