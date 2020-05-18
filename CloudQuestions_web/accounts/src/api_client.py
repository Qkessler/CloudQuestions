import os
from googleapiclient.discovery import build


CALENDAR_API_KEY = os.environ['CALENDAR_API_KEY']
service = build('calendar', 'v3', developerKey=CALENDAR_API_KEY)

