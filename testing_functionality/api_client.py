import os
import requests
import json
from googleapiclient.discovery import build
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import httplib


CALENDAR_API_KEY = os.environ['CALENDAR_API_KEY']
service = build('calendar', 'v3', developerKey=CALENDAR_API_KEY)
scope_events = 'https://www.googleapis.com/auth/calendar.events'


def calendar_connection():
    flags = tools.argparser.parse_args([])
    FLOW = OAuth2WebServerFlow(
        client_id='xxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com',
        client_secret='xxxxxx',
        scope='https://www.googleapis.com/auth/calendar',
        user_agent='<application name>'
    )
    storage = Storage('calendar.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
        credentials = tools.run_flow(FLOW, storage, flags)            
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = discovery.build('calendar', 'v3', http=http)
    
    return service

    

if __name__ == '__main__':
    request = service.calendarList().list().execute()
    # data = request.json()
    # print(data)
    # events = service.events()
    # print(events)
