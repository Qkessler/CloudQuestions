import os
import httplib2
from googleapiclient.discovery import build
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage


CALENDAR_API_KEY = os.environ['CALENDAR_API_KEY']
SCOPE_EVENTS = 'https://www.googleapis.com/auth/calendar.events'


def calendar_connection():
    flow = OAuth2WebServerFlow(
        client_id=os.environ['CALENDAR_CLIENT_ID'],
        client_secret=os.environ['CALENDAR_CLIENT_SECRET'],
        scope=SCOPE_EVENTS,
        user_agent='CloudQuestions',
        redirect_uri='http://127.0.0.1:8000/accounts/settings/'
    )
    storage = Storage('test_credentials.dat')
    credentials = storage.get()
    if not credentials or credentials.invalid:
        authorize_url = flow.step1_get_authorize_url()
        print(authorize_url)
        code = input('Enter verification code: ').strip()
        credentials = flow.step2_exchange(code)
    http_base = httplib2.Http()
    http = credentials.authorize(http_base)
    service = build('calendar', 'v3', http=http)
    return service


if __name__ == '__main__':
    s = calendar_connection()
    print(s.calendarList().list().execute())
