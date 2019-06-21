#!/usr/bin/env python 
from linebot.models import *
from line_bot_api import get_api
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
from weather import *
from alert import show_alert, read_json
from pydub import AudioSegment
import speech_recognition as sr
import os
import tempfile
from template import Template

class MessageReact():
  def __init__(self,event):
    self.event = event     
    self.send = 'reply'
    self.line_bot_api, self.handler  = get_api()

  def send_to(self,message):   
    if  self.send == 'reply':
      self.line_bot_api.reply_message(self.event.reply_token, message)
    elif self.send == 'push':
      self.line_bot_api.push_message('C8911cda987a6c04e8748e0dc8c869df0',message)
    else:
      print('Unknown send type !')

  def react(self,text):
    if text.strip().split(',')[0] == "小幫手廣播":
      textlist = text.strip().split(',')
      words = ','.join(textlist[1:])

      self.send = 'push'
      exitcode = self.react(words)
      if exitcode != 0:
        message = TextSendMessage(text=words.strip().split(',')[0])
        self.send_to(message=message)

    elif text == '小幫手再見':
        if isinstance(self.event.source, SourceGroup):
            self.line_bot_api.reply_message(
                self.event.reply_token, TextSendMessage(text='再見！有需要再加入我喔！'))
            self.line_bot_api.leave_group(self.event.source.group_id)
        elif isinstance(self.event.source, SourceRoom):
            self.line_bot_api.reply_message(
                self.event.reply_token, TextSendMessage(text='再見！有需要再加入我喔！'))
            self.line_bot_api.leave_room(self.event.source.room_id)
        else:
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text="很抱歉！小幫手不能離開一對一聊天室喔！"))

    elif text == "雷達":
      url = radar()
      message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
      )
      self.send_to(message=message)
      return 0

    elif text == "氣溫":
      url = temp()
      message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
      )
      self.send_to(message=message)
      return 0

    elif text == "雨量":
      url = rain()
      message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
      )
      self.send_to(message=message)
      return 0

    elif text.strip().split(',')[0] == "衛星雲圖":
      if len(text.strip().split(',')) == 1:
        url = satellite()
      else:
        args = text.strip().split(',')
        url = satellite(args[1],args[2])        
      message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
      )
      self.send_to(message=message)
      return 0

    elif text == "平鎮天氣":
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

      message = TextSendMessage(text=content)
      self.send_to(message=message)
      return 0

    elif text == "天氣小幫手":
      # get data
      url = 'https://opendata.cwb.gov.tw/fileapi/opendata/MFC/F-C0032-031.FW50'
      resource = ur.urlopen(url)
      content = resource.read().decode('big5')

      message = TextSendMessage(text=content)
      self.send_to(message=message)
      return 0

    elif text.strip().split(',')[0] == "代禱":
      if len(text.strip().split(',')) == 1:
        content = readprayer()
        message = TextSendMessage(text=content)
        self.send_to(message=message)
        return 0
      else:
        content = writeprayer(text)
        message = TextSendMessage(text=content)
        self.send_to(message=message)
        return 0

    elif text.strip().split(',')[0] == "輸入代禱":
      content = writeprayer(text)
      message = TextSendMessage(text=content)
      self.send_to(message=message)
      return 0

    elif text == "靈命日糧":
      content = dbpost()
      message = TextSendMessage(text=content)
      self.send_to(message=message)
      return 0

    elif text == "警報":
      url = 'https://alerts.ncdr.nat.gov.tw/JSONAtomFeeds.ashx'
      data = read_json(url)['entry']
      content = show_alert(data)
      message = TextSendMessage(text=content)
      self.send_to(message=message)
      return 0

    elif text == "論壇報新聞":
      content = cctpost()
      message = TextSendMessage(text=content)
      self.send_to(message=message)
      return 0

    elif text == "團契成員檔案":
      groupID='C8911cda987a6c04e8748e0dc8c869df0'
      userID = 'Uee94d5ab36b7b6e02a774098d6d735ae'
      member_ids_res = self.line_bot_api.get_group_member_ids(groupID)

      print(member_ids_res.member_ids)
      print(member_ids_res.next)
      content = member_ids_res.member_ids
      message = TextSendMessage(text=content)
      self.send_to(message=message)
      return 0 

    elif text == "測試身份":
      groupID='C8911cda987a6c04e8748e0dc8c869df0'
      userID = 'Uee94d5ab36b7b6e02a774098d6d735ae'
      profile = self.line_bot_api.get_group_member_profile(groupID, userID)

      content = profile.display_name 
      message = TextSendMessage(text=content)
      self.send_to(message=message)
      return 0
 
    elif text.strip().split(',')[0] == "立約小卡":
      if len(text.strip().split(',')) == 1:
        content = show_temp()
        message = TextSendMessage(text=content)
        self.send_to(message=message)
        return 0
      else:
        url = commitment(text)
        message = ImageSendMessage(
          original_content_url=url,
          preview_image_url=url
        )
        self.send_to(message=message)
        return 0
 
    elif text == "金句":
      url = goldenverse()
      message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
      )
      self.send_to(message=message)
      return 0
 
    elif text == "讚美主":
      url = goldenverse('讚美')
      message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
      )
      self.send_to(message=message)
      return 0
 
    elif text == "求安慰":
      url = goldenverse('安慰')
      message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
      )
      self.send_to(message=message)
      return 0
 
    elif text == "求醫治":
      url = goldenverse('醫治')
      message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
      )
      self.send_to(message=message)
      return 0
   
    elif text.strip().split(',')[0] == "聚會":
      if len(text.strip().split(',')) == 1:
        content = attend_show()
        message = TextSendMessage(text=content)
        self.send_to(message=message)
        return 0
      else:
        content = attend_write(text)
        message = TextSendMessage(text=content)
        self.send_to(message=message)
        return 0  

    elif text.strip().split(',')[0] == "輸入聚會":
      content = attend_write(text)
      message = TextSendMessage(text=content)
      self.send_to(message=message)
      return 0

    elif text.strip().split(',')[0] == "顯示聚會":
      content = attend_show()
      message = TextSendMessage(text=content)
      self.send_to(message=message)
      return 0

    elif text.strip().split(',')[0] == "建立聚會":
      content = attend_create(text)
      message = TextSendMessage(text=content)
      self.send_to(message=message)
      return 0

    elif text == "天氣":
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

      self.send_to(message=carousel_template_message)
    else:
      return -1

class AudioReact():
  def __init__(self,event):
    self.event = event     
    self.send = 'reply'
    self.line_bot_api, self.handler  = get_api()
    self.Temp = Template()

  def send_to(self,message):   
    if  self.send == 'reply':
      self.line_bot_api.reply_message(self.event.reply_token, message)
    elif self.send == 'push':
      self.line_bot_api.push_message('C8911cda987a6c04e8748e0dc8c869df0',message)
    else:
      print('Unknown send type !')

  def speech2text(self):
    r = sr.Recognizer()
    message_content = self.line_bot_api.get_message_content(self.event.message.id)
    ext = 'mp3'
    try:
        with tempfile.NamedTemporaryFile(prefix=ext + '-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name
        path = tempfile_path
        AudioSegment.converter = '/app/vendor/ffmpeg/ffmpeg'
        sound = AudioSegment.from_file_using_temporary_files(path)
        path = os.path.splitext(path)[0]+'.wav'
        sound.export(path, format="wav")
        with sr.AudioFile(path) as source:
            audio = r.record(source)
    except Exception as e:
        t = '音訊有問題'+test+str(e.args)+path
        message = TextSendMessage(text=t)
        self.send_to(message)
    os.remove(path)
    text = r.recognize_google(audio,language='cmn-Hant-TW')
    print(text)
    message = self.Temp.audio_template(text)
    self.send_to(message)


