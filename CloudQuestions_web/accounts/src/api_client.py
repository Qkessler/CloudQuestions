import os
import httplib2
from googleapiclient.discovery import build
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage


CALENDAR_API_KEY = os.environ['CALENDAR_API_KEY']
SCOPE_EVENTS = 'https://www.googleapis.com/auth/calendar.events'
day_colors = {
    'red': 1,
    'yellow': 3,
    'green': 5
}


def get_flow():
    flow = OAuth2WebServerFlow(
        client_id=os.environ['CALENDAR_CLIENT_ID'],
        client_secret=os.environ['CALENDAR_CLIENT_SECRET'],
        scope=SCOPE_EVENTS,
        user_agent='CloudQuestions',
        redirect_uri='http://127.0.0.1:8000/accounts/settings/'
    )
    return flow


def get_url(flow):
    authorize_url = flow.step1_get_authorize_url()
    return authorize_url


def calendar_connection(code, flow):
    credentials = flow.step2_exchange(code)
    http_base = httplib2.Http()
    http = credentials.authorize(http_base)
    service = build('calendar', 'v3', http=http)
    return service


def create_event(topic, color, service):
    event_colors = [str(num+1) for num in range(11)]
    event = {
        'summary': 'AR ' + topic,
        'description': 'This is an event created by CloudQuestions',
        'start': {
            'dateTime': '2015-05-28T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2015-05-28T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'attendees': [
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    print(event)
    # service.events().insert(calendarId='primary', event=event).execute()
