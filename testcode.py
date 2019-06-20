
def pattern_mega(text):
    patterns = [
        'mega', 'mg', 'mu', 'ＭＥＧＡ', 'ＭＥ', 'ＭＵ',
        'ｍｅ', 'ｍｕ', 'ｍｅｇａ', 'GD', 'MG', 'google',
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
        
def eyny_movie():
    target_url = 'http://www.eyny.com/forum-205-1.html'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = bf(res.text, 'html.parser')
    content = ''
    for titleURL in soup.select('.bm_c tbody .xst'):
        if pattern_mega(titleURL.text):
            title = titleURL.text
            if '11379780-1-3' in titleURL['href']:
                continue
            link = 'http://www.eyny.com/' + titleURL['href']
            data = '{}\n{}\n\n'.format(title, link)
            content += data
    return content

def panx():
    target_url = 'https://panx.asia/'
    print('Start parsing ptt hot....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = bf(res.text, 'html.parser')
    content = ""
    for data in soup.select('div.container div.row div.desc_wrap h2 a'):
        title = data.text
        link = data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content

def magazine():
    target_url = 'https://www.cw.com.tw/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = bf(res.text, 'html.parser')
    temp = ""
    for v ,date in enumerate(soup.select('.caption h3 a'),0):
        url = date['href']
        title = date.text.strip()
        temp += '{}\n{}\n'.format(title,url)
        if(v&gt;4):
            break
    return temp
def lottery():
    name = ['ltobig','lto539','lto']
    for i in name:
        url = 'https://www.pilio.idv.tw/{}/drawlist/drawlist.asp'.format(i)
        res = requests.get(url)
        res.encoding = 'utf-8'
        soup = bf(res.text,'html.parser')
        t = soup.select('.inner td')
        if i == 'ltobig':
            big = [t[i].text.strip() for i in range(4,10,1)]
        elif i == 'lto539':
            b539 = [t[i].text.strip() for i in range(3,7,1)]
        elif i == 'lto':
            bwei = [t[i].text.strip() for i in range(3,7,1)]

    return big,b539,bwei

def lottery_stat(type_lottery,year):
    if type_lottery == 'big-lotto':
        div = 4
    elif type_lottery == 'power':
        div = 5
    elif type_lottery == 'daily539':
        div = 7
    url = 'http://lotto.auzonet.com/lotto_balllist_{}_{}.html'.format(type_lottery,year)
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = bf(res.text,'html.parser')
    num = ''
    for c,i in enumerate(soup.select('.forumline tr td')[3:],1):
        if c%3 == 2:
            continue
        elif c%3 == 1:
            num += ' '+i.text.strip()+'         '
        else:
            if len(i.text.strip()) &lt; 2:
                num += '0{}次   {}\n'.format(i.text.strip(),'&#127880;️'*((int(i.text.strip()))//div))         
            else:
                num += '{}次   {}\n'.format(i.text.strip(),'&#127880;️'*((int(i.text.strip()))//div))          
    return num

def lottery_all_num(type_lottery):
    if type_lottery == 'big-lotto':
        type_lottery = 'listltobigbbk'
        start = 4
        div = 4
    elif type_lottery == 'power':
        type_lottery =  'listlto'
        start = 4
        div = 4
    elif type_lottery == 'daily539':
        type_lottery = 'listlto539bbk'
        start = 3
        div = 3
    url = 'https://www.lotto-8.com/{}.asp'.format(type_lottery)
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = bf(res.text,'html.parser')
    num = ''
    for c,i in enumerate(soup.select('.auto-style4 tr td')[start:],1):
        if c % div == 1:
            num += i.text.strip()
        elif c % div == 2:
            num += '    {}\n'.format(i.text.strip())
        elif c % div == 3:
            if type_lottery == 'listltobigbbk':
                num += '&#128176;️特別號 : {}\n'.format(i.text.strip())
            elif type_lottery == 'listlto':
                num += '&#128176;️第二區 : {}\n'.format(i.text.strip())
    return num

def lottery_year(type_lottery):
    if type_lottery == 'big-lotto':
        t = '大樂透'
    elif type_lottery == 'power':
        t = '威力彩'
    elif type_lottery == 'daily539':
         t = '今彩539'
    Carousel_template = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/zp75S87.jpg',
                title=t+'--各個年份的統計',
                text='請選擇年份',
                actions=[
                    PostbackTemplateAction(
                        label='2019',
                        data='ball_st/{}/{}'.format('2019',type_lottery)
                    ),
                    PostbackTemplateAction(
                        label='2018',
                        data='ball_st/{}/{}'.format('2018',type_lottery)
                    ),
                    PostbackTemplateAction(
                        label='2017',
                        data='ball_st/{}/{}'.format('2017',type_lottery)
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/zp75S87.jpg',
                title='各個年份的統計',
                text='請選擇年份',
                actions=[
                    PostbackTemplateAction(
                        label='2016',
                        data='ball_st/{}/{}'.format('2016',type_lottery)
                    ),
                    PostbackTemplateAction(
                        label='2015',
                        data='ball_st/{}/{}'.format('2015',type_lottery)
                    ),
                    PostbackTemplateAction(
                        label='2014',
                        data='ball_st/{}/{}'.format('2014',type_lottery)
                    ),
                ]
            )
        ]
    )
    )
    return Carousel_template           

def check_pic(img_id):
    Confirm_template = TemplateSendMessage(
    alt_text='要給你照片標籤描述嗎?',
    template=ConfirmTemplate(
    title='注意',
    text= '要給你照片標籤描述嗎?\n要就選Yes,並且回覆\n--&gt;id+描述訊息(這張照片id是'+ str(img_id) +')',
    actions=[                              
            PostbackTemplateAction(
                label='Yes',
                text='I choose YES',
                data='action=buy&amp;itemid=1'
            ),
            MessageTemplateAction(
                label='No',
                text='I choose NO'
            )
        ]
    )
    )
    return Confirm_template


def look_up(tex):
    content = ''
    target_url = 'https://tw.dictionary.search.yahoo.com/search;_ylt=AwrtXG86cTRcUGoAESt9rolQ?p={}&amp;fr2=sb-top'.format(tex)
    res =  requests.get(target_url)
    soup = bf(res.text,'html.parser')
    try:
        content += '{}\n'.format(soup.select('.lh-22.mh-22.mt-12.mb-12.mr-25.last')[0].text)
        for i in soup.select('.layoutCenter .lh-22.mh-22.ml-50.mt-12.mb-12'):
            if i.select('p  span') != []:   
                content += '{}\n{}\n'.format(i.select('.fz-14')[0].text,i.select('p  span')[0].text)
            else:
                content += '{}\n'.format(i.select('.fz-14')[0].text)
        if content == '':
            for i in soup.select('.layoutCenter .ml-50.mt-5.last'):
                content += i.text
    except IndexError:
        content = '查無此字'
    return content

def get_total_flex(body_content,footer_content=[ButtonComponent(style='link',action=URIAction(label='My github', uri='https://github.com/kevin1061517?tab=repositories'))]):
    bubble = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=body_content
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents= footer_content
            )
        )
    return bubble

def integer_word(word):
    content = look_up(word)
    if content != '查無此字':
        content = [TextComponent(text='&#128269;英文單字查詢',weight='bold', align='center',size='md',wrap=True,color='#000000'),SeparatorComponent(margin='lg'),TextComponent(text=content, size='sm',wrap=True,color='#000000')]
        audio_button = [
                    SeparatorComponent(),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=PostbackAction(label='&#128226; 美式發音', data='audio/{}'.format(word))
                    )
                    ]
        bubble = get_total_flex(content,audio_button)
        message = FlexSendMessage(alt_text="hello", contents=bubble)
    else:
        message = TextSendMessage(text=content)
    return message

def process_draw(user_id):
        start = fb.get('/{}/start'.format(user_id),None)
        if not start:
            start = 0
        else:
            start = list(start.values())[0]
        end = fb.get('/{}/end'.format(user_id),None)
        if not end:
            end = 0
        else:
            end = list(end.values())[0]
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text= '抽數字',size='xl',color='#000000'),
                    TextComponent(text= '按照步驟來隨機產生幸運數字', size='sm',color='#888888'),
                    # review
                    SeparatorComponent(color='#000000'),
                    # info
                    BoxComponent(
                        layout='vertical',
                        color = '#FFFF00',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(
                                        text='起始',
                                        color='#000000',
                                        size='xxl',
                                        flex = 5
                                    ),
                                    TextComponent(
                                        text=str(start),
                                        size='xxl',
                                        flex = 5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(
                                        text='結束',
                                        color='#000000',
                                        size='xxl',
                                        flex = 5
                                    ),
                                    TextComponent(
                                        text=str(end),
                                        size='xxl',
                                        flex = 5
                                    )
                                ],
                            )
                        ],
                    ),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='xs',
                contents=[
                    # websiteAction
                    ButtonComponent(
                        style='secondary',
                        color='#FFEE99',
                        height='sm',
                        action=MessageAction(label='設定起始數字',text='請輸入起始數字-----------')
                    ),
                    SeparatorComponent(color='#000000'),
                    # websiteAction
                    ButtonComponent(
                        style='secondary',
                        color='#FFEE99',
                        height='sm',
                        action=MessageAction(label='設定結束數字(包含)',text='請輸入結束數字-----------')
                    ),
                    SeparatorComponent(color='#000000'),
                    # websiteAction
                    ButtonComponent(
                        style='secondary',
                        color='#FFEE99',
                        height='sm',
                        action=PostbackAction(label='開始抽籤',text='抽籤結果!!',data='random/{}/{}'.format(start,end))
                    )
                ]
            ),
        )
        return bubble
    
def process_choose(user_id):
    temp_opti =[]
    texts = ''
    temp_ques = '' 
    t = fb.get('/{}/opti_num'.format(user_id),None)
    if t :
         temp = list(t.values())[0]
         temp_opti = temp.split('；')
         
    t1 = fb.get('/{}/ques_num'.format(user_id),None)
    if t1:
        temp_ques = list(t1.values())[0]
    print('-----in------')
    for i in temp_opti:
        texts += '{}\n'.format(i)
    bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text= '確定好就按下面的抽籤按鈕', weight='bold',size='lg',color='#000000'),
                    TextComponent(text= '問題為--&gt;{}'.format(temp_ques), size='md',wrap=True,color='#000000'),
                    # review
                    SeparatorComponent(color='#000000'),
                    # info
                    BoxComponent(
                        layout='vertical',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(
                                        text='選項:',
                                        color='#000000',
                                        gravity='center',
                                        flex = 1,
                                        size='lg'
                                    ),
                                    TextComponent(
                                        text='{}\n'.format(texts[:-1]),
                                        color='#000000',
                                        wrap=True,
                                        flex = 4,
                                        size='lg')
                                    ]
                            )
                        ],
                    ),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='xs',
                contents=[
                    ButtonComponent(
                        style='secondary',
                        color='#FFDD55',
                        height='sm',
                        action=PostbackAction(label='隨機選擇',data='custom')
                    ),
                    ButtonComponent(
                        style='secondary',
                        color='#FFDD55',
                        height='sm',
                        action=MessageAction(label='設定問題',text='請輸入要設定抉擇的問題:')
                    ),
                    ButtonComponent(
                        style='secondary',
                        color='#FFDD55',
                        height='sm',
                        action=MessageAction(label='設定選項',text='請輸入要設定的選項，各個選項以分號區隔!!!')
                    )
                ]
            ),
        )
    return bubble
def answer(num,user_id):
    t = fb.get('/{}/question/no'.format(user_id),None)
    if  t:
        answer = [['Secret'],['是','不是，來過好幾次'],['約會','聚餐','朋友聚','家人聚餐'],['排骨套餐','雞排套餐','銷魂叉燒飯','黯然消魂炒飯','螞蟻上樹'],
                  ['太鹹了','太清淡了','不好吃','好吃沒話講'],['價格公道','太貴了','普普通通'],['非常滿意','滿意','尚可','差勁','非常差勁'],['非常滿意','滿意','尚可','差勁','非常差勁'],['感覺很棒','感覺很差','食物好吃!','沒有']]
        answer_list = answer[num]
        content = []
        for i in answer_list:
            content += [QuickReplyButton(action=MessageAction(label=i, text=i))]
        message = QuickReply(items=content)
        return message
def questionnaire(num,user_id):
    if num == 9:
        num = 0
    t = fb.get('/{}/question/no'.format(user_id),None)
    if  t:
#        profile = line_bot_api.get_profile(event.source.user_id)
#        user_name = profile.display_name
        question = ['用餐編號','第一次來用餐?','用餐的目的是?','享用主餐的部份是?','對餐廳提供的菜餚口味感到?','對餐廳食物的價格感到?','對工作人員的服務態度感到?','餐廳衛生評價是?','想對我們建議的話']  
        return question[num]
    else:
        return None

def greet():
    t = ['哇!!感謝您的答案','太棒了!!','很寶貴的建議','我們會持續改進','謝謝您的建議','很特別的意見','會不斷提供最好服務給您','給我們持續改善的動力','真的是很寶貴的建議','謝謝您!','謝謝指教','中獎']
    r = random.randint(0,10)
    if t[r] == '中獎':
        message = ImageSendMessage(
                original_content_url='https://i.imgur.com/d9jnyyN.jpg',
                preview_image_url='https://i.imgur.com/d9jnyyN.jpg')
    else:
        message = TextSendMessage(text=t[r])
    return message

def keep(t):
        #GDriveJSON就輸入下載下來Json檔名稱
        #GSpreadSheet是google試算表名稱
        GDriveJSON = 'My First Project-9cf8421ad126.json'
        GSpreadSheet = 'BotTest'
        try:
                scope =  ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
                key = SAC.from_json_keyfile_name(GDriveJSON, scope)
                gc = gspread.authorize(key)
                worksheet = gc.open(GSpreadSheet).sheet1
        except Exception as ex:
                print('無法連線Google試算表', ex)
                sys.exit(1)
        worksheet.append_row(t)
        print('新增一列資料到試算表' ,GSpreadSheet)
def delete_row():
    #GDriveJSON就輸入下載下來Json檔名稱
        #GSpreadSheet是google試算表名稱
        GDriveJSON = 'My First Project-9cf8421ad126.json'
        GSpreadSheet = 'BotTest'
        try:
                scope =  ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
                key = SAC.from_json_keyfile_name(GDriveJSON, scope)
                gc = gspread.authorize(key)
                worksheet = gc.open(GSpreadSheet).sheet1
        except Exception as ex:
                print('無法連線Google試算表', ex)
                sys.exit(1)

        worksheet.delete_row(1)
        print('delete一列資料到試算表' ,GSpreadSheet)

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
def quest_template(answer,user_name):
    t = fb.get('/{}/question/item'.format('U19df1f98bcf1414ec15f9dad09b9b0cb'),None)
 
    answer = ''
    value = list(t.values())
    for v in value:
        for key,value in v.items():
            answer += '{} \n---&gt; {}\n\n'.format(key,value)
    bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text= '{}的消費體驗'.format(user_name), weight='bold',size='xl',color='#000000'),
                    TextComponent(text= '您的建議與指教是推動我們前進的動力，{}的滿意就是我們的努力目標，歡迎給我們寶貴的意見，感謝!!'.format(user_name),size='sm',wrap = True,color='#888888'),
                    SeparatorComponent(color='#000000'),
                    # info
                    BoxComponent(
                        layout='vertical',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    BoxComponent(
                                         layout='horizontal',
                                         spacing='md',
                                         contents=[
                                            TextComponent(
                                                    text=answer[:-1],
                                                    color='#000000',
                                                    wrap = True,
                                                    gravity = 'center',
                                                    size='md')]
                                    )
                                ]
                            )
                        ],
                    ),
                ],
            ),
            
            footer=BoxComponent(
                layout='vertical',
                spacing='xs',
                contents=[
                    SeparatorComponent(margin='xl',color='#000000'),
                    ButtonComponent(
                        style='secondary',
                        color='#66FF66',
                        height='sm',
                        action=PostbackAction(label='確定送出',data='send')
                    ),
                    ButtonComponent(
                        style='secondary',
                        color='#66FF66',
                        height='sm',
                        action=PostbackAction(label='清除資料',data='clear')
                    )
                ]
            ),
        )
    message = FlexSendMessage(alt_text="hello", contents=bubble)
    return message
    
    
@handler.add(PostbackEvent)
def handle_postback(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name
    temp = event.postback.data
    if temp[:5] == 'audio':
        t = temp.split('/')
        word = t[1]
        url = 'https://s.yimg.com/bg/dict/dreye/live/f/{}.mp3'.format(word)
        line_bot_api.reply_message(
                event.reply_token,
                AudioSendMessage(original_content_url=url,duration=3000)
            )
    elif temp == 'datetime':
        time = event.postback.params['datetime']
        t = str(time).replace('T','  ')
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text='請問來店人數為?',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=PostbackAction(label="1人",text='您訂位時間為{}\n人數為{}人'.format(t,1),data="reservation1")
                                ),
                            QuickReplyButton(
                                action=PostbackAction(label="2人",text='您訂位時間為{}\n人數為{}人'.format(t,2), data="reservation2")
                                ),
                            QuickReplyButton(
                                action=PostbackAction(label="3人",text='您訂位時間為{}\n人數為{}人'.format(t,3), data="reservation3")
                                ),
                            QuickReplyButton(
                                action=PostbackAction(label="4人",text='您訂位時間為{}\n人數為{}人'.format(t,4), data="reservation4")
                                )
                        ])
                )
        )
    elif temp == 'question':
        fb.put('/{}/question'.format(event.source.user_id),data={'no':'1'},name='no')

        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='感謝您的用餐，請先輸入您的用餐編號\n讓小弟可以為你服務')
            )
    elif temp == 'send':
        t = fb.get('/{}/question/item'.format(event.source.user_id),None)
        if not t:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='已經送出囉'))
            return
        temp = [list(i.values())[0] for i in t.values()]
        keep(temp)    
        fb.delete('/{}/question'.format(event.source.user_id),None)
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='小弟已經把貴賓{}的意見傳給公司了，我們會持續不斷改進，以顧客滿意至極'.format(user_name))
            )
    elif temp == 'clear':
        fb.delete('/{}/question'.format(event.source.user_id),None)
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='親愛的{} 小弟期待您再給我們意見'.format(user_name))
            )  
    elif temp == 'revise':
        fb.delete('/{}/member'.format(event.source.user_id),None)
    elif temp == 'custom':
        t = fb.get('/{}/opti_num'.format(event.source.user_id),None)
        bubble = process_choose(event.source.user_id)
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        if t :
            temp = list(t.values())[0]
            temp_opti = temp.split('；')
        else:
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text='必須要有輸入有正確的選項喔'),message]
            )
        result = random.choice(temp_opti)
        t1 = fb.get('/{}/ques_num'.format(event.source.user_id),None)
        if t1:
            temp_ques = list(t1.values())[0]
        else:
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text='必須要有輸入有正確的問題喔'),message]
            )
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text= '隨機結果出爐', weight='bold',size='xl',color='#000000'),
                    TextComponent(text= '如有其他問題再按下面按鈕&#128591;', size='md',color='#888888'),
                    # review
                    SeparatorComponent(color='#000000'),
                    # info
                    BoxComponent(
                        layout='vertical',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    BoxComponent(
                                         layout='baseline',
                                         spacing='sm',
                                         contents=[
                                            TextComponent(
                                                    text='問題:',
                                                    color='#000000',
                                                    gravity = 'center',
                                                    size='lg'),
                                            TextComponent(
                                                    text=temp_ques,
                                                    color='#000000',
                                                    size='lg')]
                                    ),
                                    BoxComponent(
                                         layout='baseline',
                                         spacing='sm',
                                         contents=[
                                            TextComponent(
                                                    text='隨機選項:',
                                                    color='#000000',
                                                    gravity = 'center',
                                                    size='lg'),
                                            TextComponent(
                                                    text=result,
                                                    color='#000000',
                                                    size='lg')]
                                    )
                                ]
                            )
                        ],
                    ),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='xs',
                contents=[
                    ButtonComponent(
                        style='secondary',
                        color='#FFDD55',
                        height='sm',
                        action=PostbackAction(label='其他猶豫問題',data='choose')
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
                event.reply_token,
                message)
        
    elif temp[:5] == 'first':
        print('--------in-----')
        temp = temp.split('/')
        _type = temp[1]
        text = ''
        text = '開始'
        action = PostbackAction(label='開始選擇',data='first/{}/start'.format(_type),text='為你選出最佳選擇')
        color = ['#AAAAAA','#AAAAAA']
        point = ['&#128072;','&#128072;']
        if  _type == 'yesno':
            t = ['要','不要']
        elif _type == 'buy':
            t = ['買','不買']
        elif _type == 'yes':
            t = ['是','不是']

        if 'start' in temp:
            text = '其他選擇'
            r = random.randint(0,1)
            print('----------'+str(r))
            point[r] = ' '
            color[1-r] = '#000000'
            action = MessageAction(label='其他選擇',text='choose')
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text= '隨機選擇',gravity='center',size='xl',color='#000000'),
                    TextComponent(text= '{}請按最下面按鈕'.format(text), size='sm',gravity='center',color='#888888'),
                    # review
                    SeparatorComponent(color='#000000'),
                    # info
                    BoxComponent(
                        layout='vertical',
                        color = '#FFFF00',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(
                                        text=t[0],
                                        color=color[0],
                                        size='xl',
                                        flex = 5
                                    ),
                                    TextComponent(
                                        text=point[0],
                                        size='xl',
                                        flex = 5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(
                                        text=t[1],
                                        color=color[1],
                                        size='xl',
                                        flex = 5
                                    ),
                                    TextComponent(
                                        text=point[1],
                                        size='xl',
                                        flex = 5
                                    )
                                ],
                            )
                        ],
                    ),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='xs',
                contents=[
                    # websiteAction
                    ButtonComponent(
                        style='secondary',
                        color='#FFEE99',
                        height='sm',
                        action=action
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif temp[:6] == 'random':
        profile = line_bot_api.get_profile(event.source.user_id)
        user_name = profile.display_name
        user_id = event.source.user_id
        bubble = process_draw(user_id)
        t = temp.split('/')
        start = int(t[1])
        end = int(t[2])
        if start &gt;= end:
             message = FlexSendMessage(alt_text="hello", contents=bubble)
             line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text='咦!{}要注意起始不能大於等於最後一個數字喔!!'.format(user_name)),message])
             return
        r = random.randint(start,end)
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text= '隨機選擇',size='xl',color='#000000'),
                    TextComponent(text= '&#128276;&#128276;&#128276;', size='sm'),
                    # review
                    SeparatorComponent(color='#000000'),
                    # info
                    BoxComponent(
                        layout='vertical',
                        color = '#FFFF00',
                        spacing='sm',
                        contents=[
                                    TextComponent(
                                        text='由{}到{}隨機產生的號碼'.format(start,end),
                                        color='#000000',
                                        size='lg',
                                        flex = 5
                                    ),
                                    BoxComponent(
                                        layout='baseline',
                                        color = '#FFFF00',
                                        spacing='sm',
                                        contents=[
                                               TextComponent(
                                                       text=' ',
                                                       color='#000000',
                                                       size='xl',
                                                       flex = 4
                                                ),
                                                TextComponent(
                                                       text=str(r),
                                                       color='#000000',
                                                       weight = 'bold',
                                                       size='xxl',
                                                       flex = 5
                                                )
                                        ]
                                    )        
                        ],
                        
                    ),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='xs',
                contents=[
                    # websiteAction
                    ButtonComponent(
                        style='secondary',
                        color='#FFEE99',
                        height='sm',
                        action=PostbackAction(label='再抽一次',text='抽籤結果!!',data='random/{}/{}'.format(start,end))
                    ),
                    ButtonComponent(
                        style='secondary',
                        color='#FFEE99',
                        height='sm',
                        action=MessageAction(label ='重設範圍',text='draw',)
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif temp[:6] == 'choose':
        fb.delete('/{}/opti_num'.format(event.source.user_id),None)
        fb.delete('/{}/ques_num'.format(event.source.user_id),None)
        print('in')
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text= '把老天爺幫你選擇的選項回覆給我', weight='bold',wrap=True,size='lg',color='#000000'),
                    TextComponent(text= '請先設定問題為什麼，再去設定選項，在最下面的按鈕可以點選並設定，內建有常用的選擇內容，可以參考看看', size='md',wrap=True,color='#888888'),
                    # review
                    SeparatorComponent(color='#000000'),
                    # info
                    BoxComponent(
                        layout='vertical',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(
                                        text='問題:\n選擇飲料店:',
                                        color='#000000',
                                        wrap=True,
                                        size='md'
                                    ),
                                    TextComponent(
                                        text='選項:\n50嵐;清新;coco;茶湯會',
                                        wrap=True,
                                        color='#000000',
                                        size='md'
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(
                                        text='問題:\n選擇雞排店',
                                        color='#000000',
                                        wrap=True,
                                        size='md'
                                    ),
                                    TextComponent(
                                        text='選項:\n豪大;派克;蔥Ya雞;胖老爹',
                                        color='#000000',
                                        wrap=True,
                                        size='md'
                                    )
                                ],
                            ),
                            SeparatorComponent(color='#000000')
                        ],
                    ),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='xs',
                contents=[
                    ButtonComponent(
                        style='secondary',
                        color='#FFDD55',
                        height='sm',
                        action=PostbackAction(label='內建問題',data='other',text='請選擇一下喔~')
                    ),
                    ButtonComponent(
                        style='secondary',
                        color='#FFDD55',
                        height='sm',
                        action=MessageAction(label='設定問題',text='請輸入要設定抉擇的問題:')
                    ),
                    ButtonComponent(
                        style='secondary',
                        color='#FFDD55',
                        height='sm',
                        action=MessageAction(label='設定選項',text='請輸入要設定的選項，各個選項以分號區隔喔!!!')
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif temp == 'other':
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text= '請把選擇需要解決的選擇', weight='bold',size='xl',color='#000000'),
                    TextComponent(text= '希望能夠解決你的選擇障礙...', size='md',wrap=True,color='#888888'),
                    # review
                    SeparatorComponent(color='#000000'),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='xs',
                contents=[
                    ButtonComponent(
                        style='secondary',
                        color='#5555FF',
                        height='sm',
                        action=PostbackAction(label='內建問題',data='other',text='請選擇一下喔~')
                    ),
                    ButtonComponent(
                        style='secondary',
                        color='#5555FF',
                        height='sm',
                        action=MessageAction(label='設定問題',text='請輸入要設定抉擇的問題:')
                    ),
                    SeparatorComponent(color='#000000'),
                    ButtonComponent(
                        style='secondary',
                        color='#5555FF',
                        height='sm',
                        action=MessageAction(label='設定選項',text='請輸入要設定的選項，各個選項以分號區隔~')
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
            
    elif temp == 'result':     
        print('-------in---')
        t = temp.split('/')
        lot_year = t[1]
        lot_type = t[2]
        num = lottery_stat(lot_type,lot_year)
        if lot_type == 'big-lotto':
            t = '大樂透'
        elif lot_type == 'power':
            t = '威力彩'
        elif lot_type == 'daily539':
            t = '今彩539'
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='爬蟲程式抓取奧索樂透網', size='xs',wrap=True,color='#888888'),
                    TextComponent(text= '{}年\n{}各號碼出現次數'.format(lot_year,t), weight='bold', wrap=True,size='xl',color='#000000'),
                    TextComponent(text= '各個號碼出現次數統計後的結果呈現，透過爬蟲程式免於開網頁慢慢搜尋....', size='xs',wrap=True,color='#888888'),
                    # review
                    SeparatorComponent(color='#000000'),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        color = '#FFFF00',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    TextComponent(
                                        text='號碼   出現次數',
                                        color='#000000',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text=num[:-1],
                                        color='#000000',
                                        size='md',
                                        wrap=True
                                    ),
                                    SeparatorComponent(color='#000000')
                                ],
                            ),          
                        ],
                    ),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='xs',
                contents=[
                    # websiteAction
                    ButtonComponent(
                        style='secondary',
                        color='#DAA520',
                        height='sm',
                        action=PostbackAction(label='其他年份號碼出現次數',data='ball_year/{}'.format(lot_type),text='請稍等...')
                    ),
                    SeparatorComponent(color='#000000'),
                    ButtonComponent(
                        style='secondary',
                        color='#DAA520',
                        height='sm',
                        action=PostbackAction(label='其他遊戲號碼出現次數',data='ballyear',text='請稍等...')
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
        
    elif temp[:7] == 'ball_st':
        print('-------in---')
        t = temp.split('/')
        lot_year = t[1]
        lot_type = t[2]
        num = lottery_stat(lot_type,lot_year)
        if lot_type == 'big-lotto':
            t = '大樂透'
        elif lot_type == 'power':
            t = '威力彩'
        elif lot_type == 'daily539':
            t = '今彩539'
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='爬蟲程式抓取奧索樂透網', size='xs',wrap=True,color='#888888'),
                    TextComponent(text= '{}年\n{}各號碼出現次數'.format(lot_year,t), weight='bold', wrap=True,size='xl',color='#000000'),
                    TextComponent(text= '各個號碼出現次數統計後的結果呈現，透過爬蟲程式免於開網頁慢慢搜尋....', size='xs',wrap=True,color='#888888'),
                    # review
                    SeparatorComponent(color='#000000'),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        color = '#FFFF00',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    TextComponent(
                                        text='號碼   出現次數',
                                        color='#000000',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text=num[:-1],
                                        color='#000000',
                                        size='md',
                                        wrap=True
                                    ),
                                    SeparatorComponent(color='#000000')
                                ],
                            ),          
                        ],
                    ),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='xs',
                contents=[
                    # websiteAction
                    ButtonComponent(
                        style='secondary',
                        color='#DAA520',
                        height='sm',
                        action=PostbackAction(label='其他年份號碼出現次數',data='ball_year/{}'.format(lot_type),text='請稍等...')
                    ),
                    SeparatorComponent(color='#000000'),
                    ButtonComponent(
                        style='secondary',
                        color='#DAA520',
                        height='sm',
                        action=PostbackAction(label='其他遊戲號碼出現次數',data='ballyear',text='請稍等...')
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )

    elif temp[:9] == 'ball_year':
        print('-------in---')
        print(temp)
        t = temp.split('/')
        lot_type = t[1]
        print(lot_type+'-----------')
        Carousel_template = lottery_year(lot_type)
        line_bot_api.reply_message(event.reply_token,Carousel_template)
         
    elif temp[:8] == 'ball_num':
        print('-------in---')
        t = temp.split('/')
        lot_type = t[1]
        num = lottery_all_num(lot_type)
        if lot_type == 'big-lotto':
            t = '大樂透'
        elif lot_type == 'power':
            t = '威力彩'
        elif lot_type == 'daily539':
            t = '今彩539'
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='爬蟲程式抓取樂透雲內容', size='xs',wrap=True,color='#888888'),
                    TextComponent(text= '{}歷史開獎紀錄'.format(t), weight='bold', wrap=True,size='xl',color='#000000'),
                    TextComponent(text= '各個號碼個期紀錄，僅列出最近35筆紀錄，透過爬蟲程式免於開網頁慢慢搜尋....', size='xs',wrap=True,color='#888888'),
                    # review
                    SeparatorComponent(color='#000000'),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        color = '#FFFF00',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    TextComponent(
                                        text='    日期          {}中獎號碼'.format(t),
                                        color='#000000',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text=num,
                                        color='#000000',
                                        size='xs',
                                        wrap=True
                                    ),
                                    SeparatorComponent(color='#000000')
                                ],
                            ),          
                        ],
                    ),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='xs',
                contents=[
                    # websiteAction
                    ButtonComponent(
                        style='secondary',
                        color='#DAA520',
                        height='sm',
                        action=MessageAction(label='近期開獎紀錄',text='lottery')
                    ),
                    SeparatorComponent(color='#000000'),
                    ButtonComponent(
                        style='secondary',
                        color='#DAA520',
                        height='sm',
                        action=PostbackAction(label='其他遊戲歷史開獎紀錄',data='ball_all_num',text='請稍等...')
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
        
    elif temp == 'ball_all_num':
        buttons_template = TemplateSendMessage(
            alt_text='歷史開獎紀錄',
            template=ButtonsTemplate(
                title='歷史開獎紀錄',
                text='請選擇要查詢的遊戲歷史開獎紀錄',
                thumbnail_image_url='https://i.imgur.com/sMu1PJN.jpg',
                actions=[
                    PostbackTemplateAction(
                        label='大樂透歷史紀錄',
                        data='ball_num/big-lotto',
                        text = '選擇了大樂透...'
                    ),
                    PostbackTemplateAction(
                        label='今彩539歷史紀錄',
                        data='ball_num/daily539',
                        text = '選擇了今彩539...'
                    ),
                    PostbackTemplateAction(
                        label='威力彩歷史紀錄',
                        data='ball_num/power',
                        text = '選擇了威力彩...'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        
    elif temp == 'ballyear':
        buttons_template = TemplateSendMessage(
            alt_text='歷年號碼出現次數',
            template=ButtonsTemplate(
                title='歷年號碼出現次數',
                text='請選擇一下',
                thumbnail_image_url='https://i.imgur.com/sMu1PJN.jpg',
                actions=[
                    PostbackTemplateAction(
                        label='大樂透統計',
                        data='ball_year/big-lotto'
                    ),
                    PostbackTemplateAction(
                        label='今彩539統計',
                        data='ball_year/power'
                    ),
                    PostbackTemplateAction(
                        label='威力彩統計',
                        data='ball_year/daily539'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
   
    elif temp == 'ball':
        big = ''
        r539 = ''
        r3 = ''
        print('---in--------')
        for i in  random.sample([str(i) for i in range(1,50)],6):
            if len(i) !=2 :
                big += '0{},'.format(i)
            else:
                big += '{},'.format(i)
        for i in random.sample([str(i) for i in range(1,40)],5):
            if len(i) !=2 :
                r539 += '0{},'.format(i)
            else:
                r539 += '{},'.format(i)
        
        for i in  random.sample([str(i) for i in range(1,39)],6):
            if len(i) !=2 :
                r3 += '0{},'.format(i)
            else:
                r3 += '{},'.format(i)
        r3 = r3[:-1] + '\n第二區:0{}'.format(random.sample([i for i in range(1,8)],1)[0])
        print(r3)
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='僅供參考', size='sm',wrap=True,color='#008844'),
                    TextComponent(text='幸運號碼', size='xxl',color='#000000'),
                    SeparatorComponent(color='#000000'),
                    # review
                    SeparatorComponent(color='#000000'),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        color = '#FFFF00',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                color = '#FFFF00',
                                contents=[
                                    TextComponent(
                                        text='大樂透',
                                        color='#000000',
                                        weight='bold',
                                        size='md',
                                        flex=2
                                    ),
                                    TextComponent(
                                        text=big[:-1],
                                        weight='bold',
                                        color='#FF3333',
                                        size='lg',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                color = '#FFFF00',
                                contents=[
                                    TextComponent(
                                        text='今彩539',
                                        color='#000000',
                                        weight='bold',
                                        size='md',
                                        flex = 2
                                    ),
                                    TextComponent(
                                        text=r539[:-1],
                                        weight='bold',
                                        color='#FF3333',
                                        size='lg',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='horizontal',
                                color = '#FFFF00',
                                contents=[
                                    TextComponent(
                                        text='威力彩',
                                        color='#000000',
                                        weight='bold',
                                        size='md',
                                        gravity = 'center',
                                        flex=2
                                    ),
                                    TextComponent(
                                        text=r3,
                                        weight='bold',
                                        color='#FF3333',
                                        size='lg',
                                        wrap=True,
                                        flex=5
                                    )
                                ],
                            ),
                            
                        ],
                    ),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='xs',
                contents=[
                    # websiteAction
                    ButtonComponent(
                        style='primary',
                        color='#DAA520',
                        height='sm',
                        action=PostbackAction(label='歷年號碼出現次數',data='ballyear',text='請稍等...')
                    ),
                    SeparatorComponent(color='#000000'),
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        color='#DAA520',
                        action=PostbackAction(label='再來一組', data='ball',text='好運到來...')
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)

        line_bot_api.reply_message(
            event.reply_token,
            message
        )

    elif temp[:8] == 'carousel':
        t = temp.split('/')
        pa = int(t[1])
        print('--------be else-------{}---{}'.format(pa,str(type(pa))))
        pa += 1
        print('--------af else-------{}'.format(pa))
        keyword = t[2]
        t = carousel_template(keyword,page=pa)
        line_bot_api.reply_message(
            event.reply_token,
            t)

    elif temp[0:6] == 'listen':
        url = temp[6:]
        if url == '音樂版權未授權~':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='音樂版權未授權~'))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                AudioSendMessage(original_content_url=url,duration=30000)
            )

    elif temp[0:4] == 'porn':
        print('------in------')
        t = temp.split('/')
        index = int(t[1])
        keyword = t[2]
        index += 1
        try:
            buttons_template = porn_video_template(keyword,index)
            line_bot_api.reply_message(event.reply_token, buttons_template)
        except IndexError:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='已經到底了喔'))
    elif temp[0:5] == 'video':
        t = temp.split('/')
        print('----t-----'+str(t))
        keyword = t[1]
        video_url = t[2]
        video_url = 'https://www.youtube.com/watch?v={}'.format(video_url)
        video_url,img = yvideo(video_url)
        line_bot_api.reply_message(
                event.reply_token,
                VideoSendMessage(
                    original_content_url=video_url,
                    preview_image_url=img))

# 處理圖片
@handler.add(MessageEvent,message=ImageMessage)
def handle_msg_img(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    tem_name = str(profile.display_name)
    img_id = 1
    t = fb.get('/pic',None)
    if t!=None:
        count = 1
        for key,value in t.items():
            if count == len(t):#取得最後一個dict項目
                img_id = int(value['id'])+1
            count+=1
    try:
        message_content = line_bot_api.get_message_content(event.message.id)
        with tempfile.NamedTemporaryFile(prefix='jpg-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            fb.post('/pic',{'id':str(img_id),'user':tem_name,'describe':''})
            tempfile_path = tf.name
        path = tempfile_path
        client = ImgurClient(client_id, client_secret, access_token, refresh_token)
        config = {
            'album': album_id,
            'name' : img_id,
            'title': img_id,
            'description': 'Cute kitten being cute on'
        }
        client.upload_from_path(path, config=config, anon=False)
        os.remove(path)
        image_reply = check_pic(img_id)
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text='上傳成功'),image_reply])
    except  Exception as e:
        t = '上傳失敗'+str(e.args)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=t))


from pydub import AudioSegment
import speech_recognition as sr
@handler.add(MessageEvent,message=AudioMessage)
def handle_aud(event):
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
    message = audio_template(text)
    line_bot_api.reply_message(event.reply_token,message)


import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC

# 處理訊息:
@handler.add(MessageEvent, message=TextMessage)
def handle_msg_text(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name
    picture_url = profile.picture_url
    user_id = event.source.user_id
    n = fb.get('/{}/question/no'.format(user_id),None)
    num = 1 
    if n:
        num = int(n['no'])
#    ----------------註冊-----------------------
    register = fb.get('/{}/member'.format(user_id),None)
    if register == None:
        temp = event.message.text
        if '/' not in temp:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='注意!!少了斜線(/)'))
        t = temp.split('/')
        if len(t) &gt; 2:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='請重新輸入-多打了斜線了'))
        fb.post('/{}/member'.format(user_id),{'name':t[0],'email':t[1]})
        buttons_template = TemplateSendMessage(
                alt_text='Template',
                template=ButtonsTemplate(
                    title='註冊成功',
                    text='姓名:{}\nemail:{}\n請確定是否正確'.format(t[0],t[1]),
                    actions=[
                        MessageTemplateAction(
                            label='確認無誤',
                            text='MENU'
                        ),
                        PostbackTemplateAction(
                            label='重新輸入',
                            text='請再輸入一次，名字與email以斜線(/)區隔',
                            data='revise'
                        )
                    ]
                )
        )
        line_bot_api.reply_message(
                event.reply_token,
                buttons_template)
    
    
    t = fb.get('/{}/num'.format(user_id),None)
    number = fb.get('/{}/temp'.format(user_id),None)
#    ----------------抽數字-----------------------
    if event.message.text == '請輸入起始數字-----------':
        t = '起始數字'
        fb.post('/{}/temp'.format(user_id),'起始數字')  
    elif event.message.text == '請輸入結束數字-----------':
        t = '結束數字'
        fb.post('/{}/temp'.format(user_id),'結束數字')
    elif number:
        temp = int(event.message.text)
        if '起始數字' in list(number.values()):
            fb.post('/{}/start'.format(user_id),temp)
        else:
            fb.post('/{}/end'.format(user_id),temp)
        fb.delete('/{}/temp'.format(user_id),None)
        bubble = process_draw(user_id)
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text='{}為----&gt;{}'.format(list(number.values())[0],temp)),message])
#    -----------------自訂的問題-----------------------
    elif event.message.text == '請輸入要設定抉擇的問題:':
        fb.delete('/{}/ques_num'.format(event.source.user_id),None)
        fb.post('/{}/num'.format(user_id),'問題')  
    elif event.message.text == '請輸入要設定的選項，各個選項以分號區隔!!!':
        fb.delete('/{}/opti_num'.format(event.source.user_id),None)
        fb.post('/{}/num'.format(user_id),'選項')
    elif t:
        if '問題' in list(t.values()):
            fb.post('/{}/ques_num'.format(user_id),event.message.text)
        else:
            fb.post('/{}/opti_num'.format(user_id),event.message.text)
        fb.delete('/{}/num'.format(user_id),None)
        bubble = process_choose(user_id)
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text='{}為----&gt;{}'.format(list(t.values())[0],event.message.text)),message])
    else:
        if t != None:
                line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage(text='請輸入正確格式的問題或是選項'),TextSendMessage(text='就文字包含數字也可以&#128591;')])
        elif number != None:
                line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage(text='請輸入正確的起始及結束數字'),TextSendMessage(text='只能是數字，不能包含文字喔&#128591;')])
    if event.message.text.lower() == "eyny":
        content = eyny_movie()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))

    elif event.message.text.lower() == 'draw':
        fb.delete('/{}/end'.format(user_id),None)
        fb.delete('/{}/start'.format(user_id),None)
        print('in')
        bubble = process_draw(user_id)
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
        
    elif event.message.text.lower() == 'food':
        image_message = [ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        ) for url in ['https://i.imgur.com/5iMx8nk.jpg','https://i.imgur.com/EEy8s6m.jpg','https://i.imgur.com/RCGdggZ.jpg']]
        line_bot_api.reply_message(event.reply_token,image_message)
        
        
    elif event.message.text.lower() == 'exit' or event.message.text == '不做':
        fb.delete('/{}/question'.format(event.source.user_id),None)
        line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text='如需繼續幫我們了解您的需求，可以透過問卷讓我們了解'),TextSendMessage(text='輸入menu進入選單喔')]
            ) 
    elif event.message.text.lower() == '我吃飽了':
        fb.put('/{}/question'.format(event.source.user_id),data={'no':'1'},name='no')
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='感謝您的用餐，請先輸入您的用餐編號\n讓小弟可以為你服務')
            )    
            
    elif questionnaire(num,user_id):
        if num == 9:
            fb.post('/{}/question/item'.format(user_id),{questionnaire(num-1,user_id):event.message.text})
            flex = quest_template(answer,user_name)
            line_bot_api.reply_message(
                    event.reply_token,
                    flex)
            return
        t  = questionnaire(num,user_id)
        QuickReply = answer(num,user_id)
        g = ['那想請問','方便問一下','可以告訴我們','可以問','我們想知道']
        r = random.randint(0,4)
        t = '{}{}'.format(g[r],t)
        message = greet()
        if num == 8:
            message = TextSendMessage(text='最後一題了喔!!!!')
        fb.post('/{}/question/item'.format(user_id),{questionnaire(num-1,user_id):event.message.text})
        num += 1
        fb.put('/{}/question'.format(user_id),data={'no':num},name='no') 
        line_bot_api.reply_message(
            event.reply_token,
            [message,TextSendMessage(text='--------- 消費體驗調查 ---------\n如需跳開問卷，請輸入exit或不做'),TextSendMessage(text=t,quick_reply=QuickReply)])

    elif event.message.text.lower() == "choose":
        buttons_template = TemplateSendMessage(
            alt_text='抉擇領域template',
            template=ButtonsTemplate(
                title='抉擇類型',
                text='請選擇一下，想要老天爺替你選擇的問題',
                thumbnail_image_url='https://i.imgur.com/ISBqTUQ.jpg',
                actions=[                              
                    PostbackTemplateAction(
                        label='要不要問題',
                        data='first/yesno'
                    ),
                    PostbackTemplateAction(
                        label='買不買問題',
                        data='first/buy'
                    ),
                    PostbackTemplateAction(
                        label='是不是問題',
                        data='first/yes'
                    ),
                    PostbackTemplateAction(
                        label='新增問題',
                        data='choose'
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text=' -------已經進入抉擇領域了------- '),buttons_template])

    elif event.message.text.lower() == "menu":
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                    url='https://i.imgur.com/d1XQC5H.jpg',
                    aspectMode = 'cover',
                    aspect_ratio='10:3',
                    size='full',
                    action=URIAction(uri='http://www.ccu.edu.tw/', label='label'),
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='目錄功能', weight='bold', size='lg'),
                    TextComponent(text='感謝您使用加入本店LINE BOT',align='end',color='#AAAAAA', size='sm'),
                    SeparatorComponent(color='#000000'),
                ], 
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='xs',
                contents=[
                    # websiteAction
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        color='#00AA00',
                        action=PostbackAction(label='問卷填答',data='question')
                    ),
                    ButtonComponent(
                        style='primary',
                        color='#00AA00',
                        height='sm',
                        action=MessageAction(label='精選菜單',text='food')
                    ),
                    ButtonComponent(
                        style='primary',
                        color='#00AA00',
                        height='sm',
                        action=MessageAction(label='訂位功能',text='call')
                    ),
                    ButtonComponent(
                        style='primary',
                        color='#00AA00',
                        height='sm',
                        action=MessageAction(label='其他功能',text='else')
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
#訂位
    elif event.message.text.lower() == "call":
        date_picker = TemplateSendMessage(
            alt_text='訂位系統',
            template=ButtonsTemplate(
                text='{} 你好\n請設定一下取餐時間'.format(user_name),
                title='訂位系統',
#                thumbnail_image_url=picture_url,
                actions=[
                    DatetimePickerTemplateAction(
                        label='設定',
                        data='datetime',
                        mode='datetime',
                        initial='2017-04-01T12:30',
                        min='2017-04-01T12:30',
                        max='2099-12-31T12:30'
                    )
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            date_picker
        )
        
        
    elif event.message.text == "PanX泛科技":
        content = panx()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
    elif event.message.text.lower() == "help":
        Carousel_template = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/d1XQC5H.jpg',
                title = '功能目錄',
                text = 'Hey {} bro!\n提供額外小工具，希望您能有美好的一天'.format(user_name),
                actions=[
                    MessageTemplateAction(
                        label='餐廳資訊',
                        text= 'menu'
                    ),
                    MessageTemplateAction(
                        label='電影資訊',
                        text= 'movie'
                    ),
                    MessageTemplateAction(
                        label='新聞資訊',
                        text= 'news'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/d1XQC5H.jpg',
                title = '功能目錄',
                text = 'Hey {} bro!\n提供額外小工具，希望您能有美好的一天'.format(user_name),
                actions=[
                    MessageTemplateAction(
                        label='英文字典',
                        text= '提醒您:\n只需要在查詢英文單字後加上?即可'
                    ),
                    MessageTemplateAction(
                        label='樂透查詢',
                        text= 'lottery'
                    ),
                    MessageTemplateAction(
                        label='中正大學',
                        text= 'introduce'
                    )
                ]
            )
        ]
        )
        )
        line_bot_api.reply_message(event.reply_token,Carousel_template) 
    elif event.message.text == "近期上映電影":
        content = movie()
        template = movie_template()
        line_bot_api.reply_message(
            event.reply_token,[
                    TextSendMessage(text=content),
                    template
            ]
        )

    elif event.message.text == "觸電網-youtube":
        target_url = 'https://www.youtube.com/user/truemovie1/videos'
        rs = requests.session()
        res = rs.get(target_url, verify=False)
        soup = bf(res.text, 'html.parser')
        seqs = ['https://www.youtube.com{}'.format(data.find('a')['href']) for data in soup.select('.yt-lockup-title')]
        template = movie_template()
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=seqs[random.randint(0, len(seqs) - 1)]),
                TextSendMessage(text=seqs[random.randint(0, len(seqs) - 1)]),
                TextSendMessage(text=seqs[random.randint(0, len(seqs) - 1)]),
                template
            ])

    elif event.message.text.lower() == "movie":
        buttons_template = movie_template()
        line_bot_api.reply_message(event.reply_token, buttons_template)
        
    elif event.message.text == "蘋果即時新聞":
        content = apple_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        
    elif event.message.text.lower() == "news":
        buttons_template = TemplateSendMessage(
            alt_text='news template',
            template=ButtonsTemplate(
                title='新聞類型',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/GoAYFqv.jpg',
                actions=[
                    MessageTemplateAction(
                        label='蘋果即時新聞',
                        text='蘋果即時新聞'
                    ),
                    MessageTemplateAction(
                        label='天下雜誌',
                        text='天下雜誌'
                    ),
                    MessageTemplateAction(
                        label='PanX泛科技',
                        text='PanX泛科技'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
    elif event.message.text == "天下雜誌":
        content = magazine()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
 
    elif event.message.text.lower() == 'post':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                    url='https://i.imgur.com/qXqg5qA.jpg',
                    size='full',
                    aspect_ratio='5:3',
                    aspect_mode='cover',
                    action=URIAction(uri='https://github.com/kevin1061517', label='label'),
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='Content', weight='bold', size='xl',color='#006400'),
                    SeparatorComponent(margin='xl',color='#000000'),
                    # review
                    TextComponent(
                            text='''現在在練習python各種語法~藉由這次的project，讓我更加熟悉python語法與邏輯，這個LineBot有各種功能，可以把youtube網址拉進來，LineBot會傳來網址影片，你就可以利用右下角的下載鍵，以及抓出菜單等等功能，就可以下載到手機端了&#128540;，如下:\n語法:\n1.阿滴英文yout\n關鍵字後面加上yout，就可以抓出影片了\n2.50嵐menu\n餐廳名字後面加上menu，就可以抓出餐廳單\n3.馬英九pic\n搜尋照片關鍵字加上pic，就可以馬上幫你抓到要搜尋的照片\n -------------------- 18禁 -------------------- \n4.李宗瑞porn\n搜尋關鍵字加上porn，就可以有成人影片彈出來&#128591;''',
                            size='sm',wrap=True,color='#2E8B57'
                    ),
                    SeparatorComponent(margin='xl',color='#000000'),
                    TextComponent(
                            text='承認不勇敢 你能不能別離開很多愛不能重來 我應該釋懷在街頭徘徊 下雨時為你撐傘對你的愛成阻礙 祝福你愉快',
                            size='sm',wrap=True,color='#2E8B57'
                    ),
                    SeparatorComponent(margin='xl',color='#000000'),
                    TextComponent(
                            text='承認不勇敢 你能不能別離開很多愛不能重來 我應該釋懷在街頭徘徊 下雨時為你撐傘對你的愛成阻礙 祝福你愉快',
                            size='sm',wrap=True,color='#2E8B57'
                    ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        color = '#FFFF00',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                color = '#FFFF00',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Developer',
                                        color='#000000',
                                        weight='bold',
                                        align="end",
                                        size='xxs',
                                        flex=5
                                    ),
                                    TextComponent(
                                        text='Kevin',
                                        wrap=True,
                                        weight='bold',
                                        align="end",
                                        color='#000000',
                                        size='xxs',
                                        flex=1
                                    )
                                ],
                            ), 
                        ],
                    ),
                    SeparatorComponent(),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
#                    SpacerComponent(size='sm'),
                    # callAction
                    ButtonComponent(
                        style='primary',
                        color = '#FFFF00',
                        height='sm',
                        action=URIAction(label='CALL', uri='tel:0935593342'),
                    ),
                    # separator
                    SeparatorComponent(),
                    # websiteAction

                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)

        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif event.message.text.lower() == 'lottery':
        big,b539,bwei = lottery()
        big_txt = ''
        b539_txt = ''
        bwei = ''
        for t,c in enumerate(big,1):
            if t%3==0:
                big_txt += '特別號:'
            big_txt += str(c+'\n')
        big_txt = big_txt[:-1]
        for t,c in enumerate(b539,0):
            b539_txt +='{}\n'.format(str(c))
        b539_txt = b539_txt[:-1]
        for t,c in enumerate(big,1):
            if t%3==0:
                bwei += '二區:'
            bwei +='{}\n'.format(str(c))
        bwei = bwei[:-1]
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                    url='https://i.imgur.com/9IUzhOT.jpg',
                    aspectMode = 'cover',
                    aspect_ratio='11:3',
                    size='full',
                    backgroundColor = '#FFD700',
                    action=URIAction(uri='https://github.com/kevin1061517', label='label'),
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='祝你中獎', weight='bold', size='md'),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='xs',
                        contents=[
                            BoxComponent(
                                margin = 'sm',
                                layout='horizontal',
                                contents=[
                                   ImageComponent(
                                        url='https://i.imgur.com/T6rFvGm.png',
                                        size='md',
                                        aspect_ratio='5:5',
                                        flex=2,
                                        gravity='center',
                              
                                    ),
                                    TextComponent(
                                        text=big_txt,
                                        wrap=True,
                                        color='#666666',
                                        size='md',
                                        flex=5
                                    )
                                ],
                            ),
                            SeparatorComponent(color='#000000'),
                            BoxComponent(
                                layout='horizontal',
                                margin = 'sm',
                                contents=[
                                    ImageComponent(
                                        url='https://i.imgur.com/DQrt8Xz.png',
                                        size='md',
                                        aspect_ratio='5:5',
                                        flex=2,
                                        gravity='center'
                                     
                                    ),
                                    TextComponent(
                                        text=b539_txt,
                                        wrap=True,
                                        color='#666666',
                                        size='md',
                                        flex=5,
                                    ),
                                ],
                            ),
                            SeparatorComponent(color='#000000'),
                            BoxComponent(
                                layout='horizontal',
                                margin = 'sm',
                                contents=[
                                    ImageComponent(
                                        url='https://i.imgur.com/nXq6wrd.png',
                                        size='md',
                                        aspect_ratio='5:5',
                                        flex=2,
                                        gravity='center'
                                      
                                    ),
                                    TextComponent(
                                        text=bwei,
                                        wrap=True,
                                        color='#666666',
                                        size='md',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    SeparatorComponent(color='#000000'),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='xs',
                contents=[
                    # websiteAction
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=PostbackAction(label='歷年開獎紀錄',data='ball_all_num',text='歷年號碼~詳細內容參考至台彩官網')
                    ),
                    SeparatorComponent(color='#000000'),
                    ButtonComponent(
                        style='primary',
                        color='#DAA520',
                        height='sm',
                        action=PostbackAction(label='開門見喜&#128142;️', data='ball',text='您的幸運號碼...')
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif re.search(r'\?$',event.message.text.lower())!=None:
        keyword = event.message.text.lower()[:-1]
        keyword = keyword.replace(' ','')
        print('-----------'+keyword)
        message = integer_word(keyword)
        
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
        
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
