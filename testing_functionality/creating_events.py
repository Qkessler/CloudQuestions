import datetime
from pprint import pprint as pp


day_colors = {
    'red': 1,
    'yellow': 3,
    'green': 5
}


def create_event(topic, color):
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
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    return event
    # service.events().insert(calendarId='primary', event=event).execute()


def main():
    pp(create_event('TEST', 'red'))


if __name__ == '__main__':
    main()
