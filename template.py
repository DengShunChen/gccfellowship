from linebot.models import *

class Template(object):

  def audio_template(self,text):
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

