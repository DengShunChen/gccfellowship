#!/usr/bin/env python 
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from spreadsheet_snippets import SpreadsheetSnippets

date='2019/05/04'

# If modifying these scopes, delete the file token.pickle.
#SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
spreadsheet_id = '1L-HZDaf9ZPKkXmDkdcOAOofCzCUfOydgssGiDgFuBuA'
range_name = '感恩代禱事項!B:C'

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

# create service for google spreadsheet
service = build_service()

def get_date():

    # Call the Sheets API
    range_name = '感恩代禱事項!A2:A2'
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=range_name).execute()
    values = result.get('values', [])
   
    if not values:
        print('No data found.')
    else:
        for row in values:
          date = row[0]
    return date

def show_results(values,spreadsheet,date=''):

    date = get_date()
    strings=''
    if not values:
        print('No data found.')
    else:
        for r,row in enumerate(values):
            # Print columns A and E, which correspond to indices 0 and 4.
            try:
              if r == 0:
                strings = strings + spreadsheet + '\n'
                strings = strings + '%s  %s' % (date, '感恩代禱事項') + '\n'
                strings = strings + '🌱 %-4s: %s' % (row[0], row[1]) + '\n'
              else:
                strings = strings + '🌱 %-4s: %s' % (row[0], row[1]) + '\n'
            except:
            #  print('%2.2d. %-4.4s: %s' % (r,row[0], '<<尚未填寫>>'))
              strings = strings + '🌱 %-4s: %s' % (row[0], '<<尚未填寫>>') + '\n'

    strings = strings + '\n'
    strings = strings + '如需新增/更新代禱事項，請依照以下格式輸入：' + '\n'
    strings = strings + '代禱,姓名,代禱事項   或' + '\n'
    strings = strings + '代禱,姓名：代禱事項' + '\n'
    return strings

def readprayer():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """

    range_name='感恩代禱事項!B2:C'
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=range_name).execute()
    values = result.get('values', [])

    strings = show_results(values,spreadsheet)
    return strings

def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return i
    return i+1

def writeprayer(text):
    # using SpreadsheetSnippets class
    ss = SpreadsheetSnippets(service)

    def write_spreadsheet(values):
      range_name='感恩代禱事項!B:C'
      # check out exist file
      result_ = ss.get_values(spreadsheet_id,range_name) 
      values_ = result_.get('values', [])
 
      # check name is exist or not?
      index = index_2d(values_,name)

      range_name='感恩代禱事項!B%d:C%d' % (index+1,index+1)
      if index == None:
        result = ss.append_values(spreadsheet_id,range_name,'USER_ENTERED',values) 
      else:        
        result = ss.update_values(spreadsheet_id,range_name,'USER_ENTERED',values) 

    # input text
    textlist = text.strip().split(',')

    if len(textlist) == 3:
      name = textlist[1]
      prayer = textlist[2]
      values = [[name,prayer]]
      write_spreadsheet(values)
    elif len(textlist) == 2 :
      for line in textlist[1].split('\n'):
        if line == '':
          continue
        print(line)
        pair = line.split('：')
        name = pair[0]
        prayer = pair[1]
        values = [[name,prayer]]
        write_spreadsheet(values)
    else:
      return 'Hi 你好，想輸入代禱事項嗎？請依照以下格式輸入唷...\n代禱,姓名,代禱事項'

    strings = readprayer()

    return strings

def createprayer(text):
    # input text
    textlist = text.strip().split(',')
    if len(textlist) == 2:
      create_date = textlist[1]
    else:
      return 'Hi 你好，想建立新的代禱事項嗎？請依照以下格式輸入唷...\n建立代禱,日期(yyyy/mm/dd)'

    # using SpreadsheetSnippets class
    ss = SpreadsheetSnippets(service)

    # create a new worksheet
    date = get_date()
    worksheetname = date+'感恩代禱事項'
    result = ss.add_worksheet(spreadsheet_id,worksheetname)  

    # get historical prayers
    range_name = '感恩代禱事項!A:C'
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=range_name).execute()
    
    # copy to new worksheet
    range_name = worksheetname+'!A:C'
    result = ss.update_values(spreadsheet_id,range_name,'USER_ENTERED',result['values']) 

    # clear 
    clean=True
    if clean:
      range_name = '感恩代禱事項!B2:C'
      result = service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, 
                                                      range=range_name).execute()

    #update date 
    range_name = '感恩代禱事項!A2:A2'
    values = [[create_date]]
    result = ss.update_values(spreadsheet_id,range_name,'USER_ENTERED',values) 
    result = '您好！已備份與建立新代禱！'
    return result

if __name__ == '__main__':
  print(writeprayer('代禱,\n我是誰1:代禱事項1\n我是誰2:代禱事項2'))
  print(writeprayer('代禱,\n我是誰3:代禱事項3'))
# print(writeprayer('代禱,我是誰4,代禱事項4'))
#  print(createprayer('建立代禱,2019/08/08'))
