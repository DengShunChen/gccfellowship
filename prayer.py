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
SAMPLE_SPREADSHEET_ID = '1L-HZDaf9ZPKkXmDkdcOAOofCzCUfOydgssGiDgFuBuA'
SAMPLE_RANGE_NAME = '感恩代禱事項!B:C'

spreadsheet='https://docs.google.com/spreadsheets/d/%s/' % (SAMPLE_SPREADSHEET_ID)

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
def get_date():
    service = build_service()

    # Call the Sheets API
    range_name = 'A2:A2'
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
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
              #  print('    %-4.4s: %s %s' % (row[0], row[1]),date)
                strings = strings + spreadsheet + '\n'
                strings = strings + '    %-4.4s: %s %s' % (row[0], date, row[1]) + '\n'
              else:
             #   print('%2.2d. %-4.4s: %s' % (r,row[0], row[1]))
                strings = strings + '%2d. %-4.4s: %s' % (r,row[0], row[1]) + '\n'
            except:
            #  print('%2.2d. %-4.4s: %s' % (r,row[0], '<<尚未填寫>>'))
              strings = strings + '%2d. %-4.4s: %s' % (r,row[0], '<<尚未填寫>>') + '\n'

    strings = strings + '\n'
    strings = strings + '如需新增/更新代禱事項，請依照以下格式輸入：' + '\n'
    strings = strings + '輸入代禱,姓名,代禱事項' + '\n'
    return strings

def readprayer():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    service = build_service()

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    strings = show_results(values,spreadsheet)
    return strings

def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return i
    return i+1

def writeprayer(text):
    # input text
    textlist=text.strip().split(',')
    name = textlist[1]
    prayer = textlist[2]
    _values = [[name,prayer]]

    # create service for google spreadsheet
    service = build_service()
 
    # using SpreadsheetSnippets class
    ss = SpreadsheetSnippets(service)

    range_name='B:C'
    # check out exist file
    result = ss.get_values(SAMPLE_SPREADSHEET_ID,range_name) 
    values = result.get('values', [])
 
    # check name is exist or not?
    index = index_2d(values,name)

    range_name='B%d:C%d' % (index+1,index+1)
    if index == None:
      result = ss.append_values(SAMPLE_SPREADSHEET_ID,range_name,'USER_ENTERED',_values) 
    else:        
      result = ss.update_values(SAMPLE_SPREADSHEET_ID,range_name,'USER_ENTERED',_values) 

    print(result)
    range_name=result['updatedRange']

    result = ss.get_values(SAMPLE_SPREADSHEET_ID,range_name) 
    values = result.get('values', [])

    strings = show_results(values,spreadsheet)

    return strings

if __name__ == '__main__':
  print(writeprayer('輸入代禱,測試,測試代禱事項'))
#  print(readprayer())
