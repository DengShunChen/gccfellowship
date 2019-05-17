from flask import Flask, request, abort
import random
import configparser

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from cwb_data import *
#from google_search import *
from prayer import *
from dailybread import get_post as dbpost
from cct import get_post as cctpost
from attendance import create as attend_create
from attendance import show as attend_show
from attendance import write as attend_write
from create_card import CreateCard as commitment
from create_card import show as show_temp
from create_goldenverse import CreateCard as goldenverse
from tools import Toolbox

app = Flask(__name__)
tb = Toolbox

config = configparser.ConfigParser()
config.read("config.ini")

# Channel Access Token
line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
# Channel Secret
handler = WebhookHandler(config['line_bot']['Channel_Secret'])


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #message = TextSendMessage(text=event.message.text)
    if event.message.text == "雷達":
      
      url = 'https://www.cwb.gov.tw/Data/radar/CV1_TW_1000.png'
      tb.download_image(url,'./radar.png')
      url = tb.upload_photo('./radar.png')

      message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
      )
      line_bot_api.reply_message(event.reply_token, message)
      return 0

    if event.message.text == "氣溫":

      url = 'https://www.cwb.gov.tw/Data/temperature/temp.jpg'
      tb.download_image(url,'./temp.jpg')
      url = tb.upload_photo('./temp.jpg')

      message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
      )
      line_bot_api.reply_message(event.reply_token, message)
      return 0

    if event.message.text == "平鎮天氣":
      dataid="F-D0047-007"
      dataformat='JSON'
      # get cwb open data
      data = cwb_open_data(dataid,dataformat)
      # read json file
      data.read_json()
      # get weather information
      location='平鎮區'
      data.get_info(location)
      content = data.write_info(data.WeatherDescription)

      line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
      return 0

    if event.message.text == "天氣小幫手":
      # get data
      url = 'https://opendata.cwb.gov.tw/fileapi/opendata/MFC/F-C0032-031.FW50'
      resource = ur.urlopen(url)
      content = resource.read().decode('big5')

      line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
      return 0

    if event.message.text.strip().split(',')[0] == "代禱":
      if len(event.message.text.strip().split(',')) == 1:
        content = readprayer()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
      else:
        content = writeprayer(event.message.text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0

    if event.message.text.strip().split(',')[0] == "輸入代禱":
      content = writeprayer(event.message.text)
      line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
      return 0

    if event.message.text == "靈命日糧":
      content = dbpost()
      line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
      return 0

    if event.message.text == "論壇報新聞":
      content = cctpost()
      line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
      return 0

    if event.message.text == "團契成員檔案":
      profile = line_bot_api.get_group_member_profile(group_id, user_id)

      content = ''
      content = content + profile.display_name + '/n'
      line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
      return 0
 
    if event.message.text.strip().split(',')[0] == "立約小卡":

      if len(event.message.text.strip().split(',')) == 1:
        content = show_temp()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
      else:
        url = commitment(event.message.text)
        message = ImageSendMessage(
          original_content_url=url,
          preview_image_url=url
        )
        line_bot_api.reply_message(event.reply_token, message)
        return 0
 
    if event.message.text == "金句":
      url = goldenverse()
      message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
      )
      line_bot_api.reply_message(event.reply_token, message)
      return 0
 
    if event.message.text == "讚美主":
      url = goldenverse('讚美')
      message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
      )
      line_bot_api.reply_message(event.reply_token, message)
      return 0
 
    if event.message.text == "求安慰":
      url = goldenverse('安慰')
      message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
      )
      line_bot_api.reply_message(event.reply_token, message)
      return 0
 
    if event.message.text == "求醫治":
      url = goldenverse('醫治')
      message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
      )
      line_bot_api.reply_message(event.reply_token, message)
      return 0
   
    if event.message.text.strip().split(',')[0] == "出席":
      if len(event.message.text.strip().split(',')) == 1:
        content = attend_show()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
      else:
        content = attend_write(event.message.text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0  

    if event.message.text.strip().split(',')[0] == "輸入出席":
      content = attend_write(event.message.text)
      line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
      return 0

    if event.message.text.strip().split(',')[0] == "顯示出席":
      content = attend_show()
      line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
      return 0

    if event.message.text.strip().split(',')[0] == "建立聚會":
      content = attend_create(event.message.text)
      line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
      return 0

    if event.message.text == "天氣":
      carousel_template_message = TemplateSendMessage(
          alt_text='目錄 contains',
          template=CarouselTemplate(
              columns=[
                  CarouselColumn(
                      thumbnail_image_url='https://wi-images.condecdn.net/image/doEYpG6Xd87/crop/810/f/weather.jpg',
                      title='現在天氣',
                      text='請選擇',
                      actions=[
                          MessageAction(
                              label='雷達',
                              text='雷達'
                          ),
                          MessageAction(
                              label='氣溫',
                              text='氣溫'
                          ),
                          URIAction(
                              label='氣象局官網',
                              uri='https://www.cwb.gov.tw/V8/C/index.html'
                          )
                      ]
                  ),
                  CarouselColumn(
                      thumbnail_image_url='https://wi-images.condecdn.net/image/doEYpG6Xd87/crop/810/f/weather.jpg',
                      title='空氣品質',
                      text='請選擇',
                      actions=[
                          URIAction(
                              label='平鎮區空氣品質',
                              uri='http://aqicn.org/city/taiwan/pingzhen/hk/'
                          ),
                          URIAction(
                              label='中壢區空氣品質',
                              uri='http://aqicn.org/city/taiwan/jhongli/hk/'
                          ),
                          URIAction(
                              label='台灣空氣品質',
                              uri='https://airtw.epa.gov.tw/'
                          )
                      ]
                  )
              ]
          )
      )

      line_bot_api.reply_message(event.reply_token, carousel_template_message)

#    content = search(event.message.text)
#    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))

# 處理貼圖（隨機選擇貼圖回應）
#@handler.add(MessageEvent, message=StickerMessage)
#def handle_sticker_message(event):
#    print("package_id:", event.message.package_id)
#    print("sticker_id:", event.message.sticker_id)
#    # ref. https://developers.line.me/media/messaging-api/sticker_list.pdf
#    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105, 106,
#                   107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
#                   126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402]
#    index_id = random.randint(0, len(sticker_ids) - 1)
#    sticker_id = str(sticker_ids[index_id])
#    print(index_id)
#    sticker_message = StickerSendMessage(
#        package_id='1',
#        sticker_id=sticker_id
#    )
#    line_bot_api.reply_message(event.reply_token,sticker_message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
