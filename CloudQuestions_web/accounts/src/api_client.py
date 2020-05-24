import os
import random
from datetime import datetime, timedelta
import httplib2
from questions.src.question_service import get_color
from googleapiclient.discovery import build
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage


DEFAULT_URL = 'http://127.0.0.1:8000/'
CALENDAR_API_KEY = os.environ['CALENDAR_API_KEY']
SCOPE_EVENTS = 'https://www.googleapis.com/auth/calendar.events'


def get_flow():
    """ Creation of the web server flow given the auth
    parameters in the environment """
    flow = OAuth2WebServerFlow(
        client_id=os.environ['CALENDAR_CLIENT_ID'],
        client_secret=os.environ['CALENDAR_CLIENT_SECRET'],
        scope=SCOPE_EVENTS,
        user_agent='CloudQuestions',
        redirect_uri='http://127.0.0.1:8000/accounts/settings/'
    )
    return flow


def get_url(flow):
    """ Given the flow calculated in the get_flow function,
    creates the url for the oauth process. """
    authorize_url = flow.step1_get_authorize_url()
    return authorize_url


def calendar_connection(code, flow):
    """ Given the code that is taken from the url and the flow, sets
    up the calendar connection and returns the service. """
    credentials = flow.step2_exchange(code)
    http_base = httplib2.Http()
    http = credentials.authorize(http_base)
    service = build('calendar', 'v3', http=http)
    return service


# TODO: Get the color from topic creation, not random for consistancy.
def create_event(topic, color, service):
    """ Creation of the event for the topic after the random session ended"""
    day_colors = {
        'red': 1,
        'yellow': 3,
        'green': 7
    }
    date = datetime.now().date() + timedelta(days=day_colors.get(color))
    description = 'This is an event created by CloudQuestions as '
    description += f'a reminder to revisit the topic "{topic}" '
    description += 'in the following link: \n'
    description = description + DEFAULT_URL + 'questions/' + topic
    event = {
        'summary': 'AR ' + topic,
        'description': description,
        'start': {
            'date': str(date),
        },
        'end': {
            'date': str(date),
        },
        'colorId':
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    service.events().insert(calendarId='primary', body=event).execute()


def random_color():
    """ Returns a random color from the 11 colorIds
    supported by calendar api. """
    event_colors = [str(num+1) for num in range(11)]
    random_color = event_colors[random.randint(0, len(event_colors) - 1)]
