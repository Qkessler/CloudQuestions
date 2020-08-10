import os
import random
from datetime import datetime, timedelta
import httplib2
from questions.src import question_service
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from django.conf import settings


DEFAULT_URL = "https://cloudquestions.es/"
CALENDAR_API_KEY = settings.CALENDAR_API_KEY
SCOPE_EVENTS = "https://www.googleapis.com/auth/calendar.events"


def get_flow(topic, color):
    """ Creation of the web server flow given the auth
    parameters in the environment """
    flow = OAuth2WebServerFlow(
        client_id=settings.CALENDAR_CLIENT_ID,
        client_secret=settings.CALENDAR_CLIENT_SECRET,
        scope=SCOPE_EVENTS,
        user_agent="CloudQuestions",
        redirect_uri="https://cloudquestions.es/accounts/settings/",
        state=f"{topic}+{color}",
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
    service = build("calendar", "v3", http=http)
    return service


def create_event(topic, color, service):
    """ Creation of the event for the topic after the random session ended"""
    day_colors = {"red": 1, "yellow": 3, "green": 7}
    date = datetime.now().date() + timedelta(days=day_colors.get(color))
    description = "This is an event created by CloudQuestions as "
    description += f'a reminder to revisit the topic "{topic}" '
    description += "in the following link: \n"
    description = description + DEFAULT_URL + "questions/" + topic + "/"
    event = {
        "summary": "AR " + topic,
        "description": description,
        "start": {"date": str(date),},
        "end": {"date": str(date),},
        "colorId": question_service.get_color(topic),
        "reminders": {
            "useDefault": False,
            "overrides": [{"method": "popup", "minutes": 10},],
        },
    }
    service.events().insert(calendarId="primary", body=event).execute()


def random_color():
    """ Returns a random color from the 11 colorIds
    supported by the google calendar api. """
    event_colors = [num + 1 for num in range(11)]
    color = event_colors[random.randint(0, len(event_colors) - 1)]
    return color
