from linebot.models import *

class Template():
  def __init__(self):
    self.text = ''

  def audio_template(self,text):
    Confirm_template = TemplateSendMessage(
        alt_text='audio_template',
        template=ConfirmTemplate(
            title='確定一下吧',
            text='您說的是:\n{}'.format(text),
            actions=[
                MessageTemplateAction(
                    label='不對',
                    text='抱歉！請再說一次。'
                ),
                MessageTemplateAction(
                    label='對',
                    text=text
                )
            ]
        )
    )
    return Confirm_template

