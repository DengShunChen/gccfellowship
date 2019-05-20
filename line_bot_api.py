import configparser

from linebot import (
    LineBotApi, WebhookHandler
)

def get_api():
  config = configparser.ConfigParser()
  config.read("config.ini")

  # Channel Access Token
  line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
  # Channel Secret
  handler = WebhookHandler(config['line_bot']['Channel_Secret'])

  return line_bot_api, handler

