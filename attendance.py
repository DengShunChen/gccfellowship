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

    range_name='A2:F2'
    result = ss.get_values(spreadsheet_id,range_name) 
    values = result.get('values', [])
    strings=''
    if not values:
        print('No data found.')
    else:
        for row in values:
          strings = strings + '%s 喜樂家庭團契聚會' % (row[0]) + '\n'
          strings = strings + '🕙時間：%s ' % (row[1]) + '\n'
          strings = strings + '💒地點：%s ' % (row[2]) + '\n'
          strings = strings + '\n'
          strings = strings + '📜主題：%s ' % (row[3]) + '\n'
          strings = strings + '📣講員：%s ' % (row[4]) + '\n'
          strings = strings + '🎼詩歌：%s ' % (row[5]) + '\n'
 
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
            if row[1].strip() == '請假':
              off = off + row[0] + ', '

    strings = strings + '出席：%s' % (on) + '\n'
    strings = strings + '\n'
    strings = strings + '請假：%s' % (off) + '\n'
    strings = strings + '\n'
    strings = strings + '\n'
    strings = strings + '功能範例：' + '\n'
    strings = strings + '新增-> 建立聚會,2019/05/18,AM10:00,教會一樓會議室,分享主題,登舜,荃滿' + '\n'
    strings = strings + '查詢-> 顯示出席' + '\n'
    strings = strings + '填寫-> 輸入出席,登舜家,出席' +'\n'
    strings = strings + '\n'

    return strings

def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return i

def create(text):
    textlist=text.strip().split(',')
    date = textlist[1]
    time = textlist[2]
    position = textlist[3]
    subject = textlist[4]
    speaker = textlist[5]
    worship = textlist[6]
    _values = [[date,time,position,subject,speaker,worship]]
 
    # create service for google spreadsheet
    service = build_service()
 
    # using SpreadsheetSnippets class
    ss = SpreadsheetSnippets(service)

    # write values
    range_name='A%d:F%d' % (2,2)
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
    name = textlist[1]
    onoroff = textlist[2]
 
    if onoroff != '請假':
      onoroff = '出席'

    _values = [[name,onoroff]]

    # create service for google spreadsheet
    service = build_service()
 
    # using SpreadsheetSnippets class
    ss = SpreadsheetSnippets(service)

    # check out exist file
    range_name='A:B'
    result = ss.get_values(spreadsheet_id,range_name) 
    values = result.get('values', [])
 
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

#  print(create('建立聚會,2019/05/11,AM 10:00,教會一樓會議室,婚姻輔導課程分享與實作,嘉玲,逸農'))
#  print(show())
   print(write('輸入出席,天才家,請假'))
