#!/usr/bin/env python
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from spreadsheet_snippets import SpreadsheetSnippets

# If modifying these scopes, delete the file token.pickle.
#SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
spreadsheet_id = '1px-zh5iohWT6rNBZFNn4r_MYzmGu3St07FisKGHP6ts'

#測試用
#spreadsheet_id = '1Rg-n63tz5jE0Y26hXuROfzF9V2nNVPi_B1vFJvaDhCw'

range_name = 'A:B'

spreadsheet='https://docs.google.com/spreadsheets/d/%s/' % (spreadsheet_id)
def build_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    return service 

def show():
    # create service for google spreadsheet
    service = build_service() 
    # using SpreadsheetSnippets class
    ss = SpreadsheetSnippets(service)

    range_name='A2:G2'
    result = ss.get_values(spreadsheet_id,range_name) 
    values = result.get('values', [])
    strings=''
    if not values:
      print('No data found.')
    else:
      for row in values:
        if row[1] == '暫停':
          strings = strings + '%s 喜樂家庭團契聚會 暫停一次' % (row[0]) + '\n'
          strings = strings + '\n'
          strings = strings + '新增-> 建立聚會,2019/MM/DD,AM10:00,教會一樓會議室,分享主題,講員,詩歌,幼兒照顧' + '\n'
          return strings
        else:  
          strings = strings + '%s 喜樂家庭團契聚會' % (row[0]) + '\n'
          strings = strings + '🕙時間：%s ' % (row[1]) + '\n'
          strings = strings + '💒地點：%s ' % (row[2]) + '\n'
          strings = strings + '\n'
          strings = strings + '📜主題：%s ' % (row[3]) + '\n'
          strings = strings + '📣講員：%s ' % (row[4]) + '\n'
          strings = strings + '🎼詩歌：%s ' % (row[5]) + '\n'
          strings = strings + '👶幼兒照顧：%s ' % (row[6]) + '\n'
 
    range_name='A4:B'
    result = ss.get_values(spreadsheet_id,range_name) 
    values = result.get('values', [])
 
    strings = strings + '\n'
    on = '' 
    off= ''
    if not values:
        print('No data found.')
    else:
        for row in values:
            if row[1].strip() == '出席':
              on = on + row[0] + ', '
            else:
              off = off + row[0] + row[1][2:] + ', '

    strings = strings + '出席：%s' % (on) + '\n'
    strings = strings + '\n'
    strings = strings + '請假：%s' % (off) + '\n'
    strings = strings + '\n'
    strings = strings + '\n'
    strings = strings + '功能範例：' + '\n'
    strings = strings + '新增聚會-> 建立聚會,2019/MM/DD,AM10:00,教會一樓會議室,分享主題,講員,詩歌,幼兒照顧' + '\n'
    strings = strings + '暫停聚會-> 建立聚會,2019/MM/DD,暫停' + '\n'
    strings = strings + '查詢聚會-> 聚會' + '\n'
    strings = strings + '填寫出席-> 聚會,姓名,出席/請假' +'\n'
    strings = strings + '\n'

    return strings

def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return i

def create(text):
    textlist=text.strip().split(',')
    if len(textlist) != 8 and (len(textlist) != 3 or textlist[2] != '暫停'):
      return '團契主席好！請依照以下方式建立聚會喔:)\n新增聚會：建立聚會,2019/MM/DD,AM10:00,教會一樓會議室,分享主題,講員,詩歌,幼兒照顧\n暫停聚會：建立聚會,2019/MM/DD,暫停'

    if len(textlist) == 8:
      date = textlist[1]
      time = textlist[2]
      position = textlist[3]
      subject = textlist[4]
      speaker = textlist[5]
      worship = textlist[6]
      babysitter = textlist[7]
    elif len(textlist) == 3:
      date = textlist[1]
      time = textlist[2]
      position = textlist[2]
      subject = textlist[2]
      speaker = textlist[2]
      worship = textlist[2]
      babysitter = textlist[2]

    _values = [[date,time,position,subject,speaker,worship,babysitter]]
 
    # create service for google spreadsheet
    service = build_service()
 
    # using SpreadsheetSnippets class
    ss = SpreadsheetSnippets(service)

    # write values
    range_name='A2:G2'
    result = ss.update_values(spreadsheet_id,range_name,'USER_ENTERED',_values) 

    # clear attendance 
    range_name = 'A4:B20'
    request = service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=range_name)
    response = request.execute()

    strings = show()

    return strings

def write(text):
    # input text
    textlist=text.strip().split(',')
    if len(textlist) != 3:
      return 'Hi 你好，想輸入聚會出席與否嗎？請依照以下格式輸入唷...\n聚會,姓名,出席/請假（原因） \n 註：原因可不填'      

    name = textlist[1]
    onoroff = textlist[2]
    #check values
    if onoroff[0:2] == '出席' or onoroff[0:2] == '請假':
      _values = [[name,onoroff]]
    else:
      return '%s您好，請輸入"出席"或"請假（原因）"，謝謝您！' % (name)

    # create service for google spreadsheet
    service = build_service()
 
    # using SpreadsheetSnippets class
    ss = SpreadsheetSnippets(service)

    # check out exist file
    range_name='A:B'
    result = ss.get_values(spreadsheet_id,range_name) 
    values = result.get('values', [])

    for row in values:
      if row[1] == '暫停':
        strings = '%s平安，很抱歉唷！%s 喜樂家庭團契聚會 暫停一次！' % (name,row[0]) + '\n'
        return strings
    
    # check name is exist or not?
    index = index_2d(values,name)

    if index == None:
      range_name='A:B'
      result = ss.append_values(spreadsheet_id,range_name,'USER_ENTERED',_values) 
    else:        
      range_name='A%d:B%d' % (index+1,index+1)
      result = ss.update_values(spreadsheet_id,range_name,'USER_ENTERED',_values) 

    strings = show()

    return strings

if __name__ == '__main__':

#  print(create('建立聚會,2019/05/11,AM 10:00,教會一樓會議室,婚姻輔導課程分享與實作,嘉玲,逸農,登舜'))
#  print(create('建立聚會,2019/05/25,暫停'))
#  print(show())
   print(write('聚會,天才家,請假(肚子痛)'))
