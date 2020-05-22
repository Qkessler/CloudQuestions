from datetime import datetime, timedelta
from pprint import pprint as pp
import random


DEFAULT_URL = 'http://127.0.0.1:8000/'
day_colors = {
    'red': 1,
    'yellow': 3,
    'green': 5
}


def create_event(topic, color):
    event_colors = [str(num+1) for num in range(11)]
    date = datetime.now().date() + timedelta(days=day_colors.get(color))
    description = 'This is an event created by CloudQuestions as '
    description += f'a reminder to revisit the topic "{topic}" '
    description += 'in the following link: \n'
    decription = description + DEFAULT_URL + 'questions/' + topic
    event = {
        'summary': 'AR ' + topic,
        'description': description,
        'start': {
            'date': str(date),
        },
        'end': {
            'date': str(date),
        },
        'colorId': event_colors[random.randint(0, len(event_colors) - 1)],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    return event
    # service.events().insert(calendarId='primary', event=event).execute()


def main():
    pp(create_event('TEST', 'green'))


if __name__ == '__main__':
    main()
