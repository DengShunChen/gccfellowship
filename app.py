#!/usr/bin/env python 
from datetime import datetime, timedelta
from flask import Flask, request, abort
import random
from line_bot_api import get_api
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from reaction import MessageReact 


app = Flask(__name__)

# get Line bot API 
line_bot_api, handler = get_api()

# Deng-Shun 
userID='Uee94d5ab36b7b6e02a774098d6d735ae'

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
  # using class
  MR = MessageReact(event)
  # input message
  text = event.message.text
  # text message reaction 
  MR.react(text)

# 處理加入訊息
@handler.add(JoinEvent)
def handle_join(event):
    newcoming_text = "謝謝邀請小幫手來至此群組！！我會盡力為大家服務～"

    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=newcoming_text)
        )
    line_bot_api.push_message(
            userID,
            TextMessage(text='Hi 有群組加入小幫手了唷！')
        )
    print("JoinEvent =", event)
    print("加入的相關資訊 =", event.source)

# 處理離開訊息
@handler.add(LeaveEvent)
def handle_leave(event):
    print("leave Event =", event)
    print("我被踢掉了QQ 相關資訊", event.source)
    line_bot_api.push_message(
            userID,
            TextMessage(text='Hi 有群組離開小幫手了唷！')
        )

# 處理貼圖（隨機選擇貼圖回應）
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    print("package_id:", event.message.package_id)
    print("sticker_id:", event.message.sticker_id)
    # ref. https://developers.line.me/media/messaging-api/sticker_list.pdf
    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105, 106,
                   107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                   126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402]
    index_id = random.randint(0, len(sticker_ids) - 1)
    sticker_id = str(sticker_ids[index_id])
    print(index_id)
    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id=sticker_id
    )
#   line_bot_api.reply_message(event.reply_token,sticker_message)

# 處理內部傳送訊息
@handler.add(PostbackEvent)
def handle_postback(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name
    data = event.postback.data

# 處理音訊訊息
from pydub import AudioSegment
import speech_recognition as sr
import os
import tempfile
@handler.add(MessageEvent,message=AudioMessage)
def handle_aud(event):

    def audio_template(text):
    Confirm_template = TemplateSendMessage(
        alt_text='audio_template',
        template=ConfirmTemplate(
            title='確定一下吧',
            text='您的建議是:\n{}'.format(text),
            actions=[
                MessageTemplateAction(
                    label='錯',
                    text='那請再說一次'
                ),
                MessageTemplateAction(
                    label='對',
                    text=text
                )
            ]
        )
    )
    return Confirm_template


    r = sr.Recognizer()
    message_content = line_bot_api.get_message_content(event.message.id)
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
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=t))
    os.remove(path)
    text = r.recognize_google(audio,language='zh-TW')
    print(text)
    message = audio_template(text)
    line_bot_api.reply_message(event.reply_token,message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
