from datetime import datetime, timedelta
from flask import Flask, request, abort
import random
from line_bot_api import get_api
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from reaction import MessageReact 
#from cwb_data import *
#from google_search import *
#from prayer import *
#from dailybread import get_post as dbpost
#from cct import get_post as cctpost
#from attendance import create as attend_create
#from attendance import show as attend_show
#from attendance import write as attend_write
#from create_card import CreateCard as commitment
#from create_card import show as show_temp
#from create_goldenverse import CreateCard as goldenverse
#from weather import *
#from alert import show_alert, read_json

app = Flask(__name__)
line_bot_api, handler = get_api()

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

  # 
  if text.strip().split(',')[0] == "小幫手推播":
    message_react(text.strip().split(',')[1])

    line_bot_api.push_message(
          'C8911cda987a6c04e8748e0dc8c869df0',
           TextMessage(text=text.strip().split(',')[1])
      )


@handler.add(JoinEvent)
def handle_join(event):
    newcoming_text = "謝謝邀請小幫手來至此群組！！我會盡力為大家服務～"

    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=newcoming_text)
        )
    line_bot_api.push_message(
            'Uee94d5ab36b7b6e02a774098d6d735ae',
            TextMessage(text='Hi 有群組加入小幫手了唷！')
        )
    print("JoinEvent =", event)
    print("加入的相關資訊 =", event.source)

@handler.add(LeaveEvent)
def handle_leave(event):
    print("leave Event =", event)
    print("我被踢掉了QQ 相關資訊", event.source)
    line_bot_api.push_message(
            'Uee94d5ab36b7b6e02a774098d6d735ae',
            TextMessage(text='Hi 有群組離開小幫手了唷！')
        )



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
