from social_core.backends.google import GoogleOAuth2


class GoogleCalendarOAuth2(GoogleOAuth2):
    def get_scope(self):
        scope = super(GoogleCalendarOAuth2, self).get_scope()
        if self.data.get('extrascope'):
            scope = scope + [('calendar.events')]
        return scope
