import os
from googleapiclient.discovery import build
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import httplib2


CALENDAR_API_KEY = os.environ['CALENDAR_API_KEY']
scope_events = 'https://www.googleapis.com/auth/calendar.events'


def calendar_connection():
    flags = tools.argparser.parse_args([])
    FLOW = OAuth2WebServerFlow(
        client_id=os.environ['CALENDAR_CLIENT_ID'],
        client_secret=os.environ['CALENDAR_CLIENT_SECRET'],
        scope=scope_events,
        user_agent='CloudQuestions'
    )
    storage = Storage('calendar.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(FLOW, storage, flags)
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('calendar', 'v3', http=http)
    return service


if __name__ == '__main__':
    service = calendar_connection()
    print(service)
