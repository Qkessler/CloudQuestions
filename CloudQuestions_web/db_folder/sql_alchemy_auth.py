from sqlalchemy.orm.exc import NoResultFound
from Overseer import models


class SQLAlchemyUserBackend(object):
    supports_anonymous_user = True
    supports_inactive_user = True

    def __init__(self):
        self.session = models.Session()

    def authenticate(self, username=None, password=None):
        try:
            user = self.session.query(
                models.User).filter_by(username=username).one()
            if user.check_password(password):
                return user
        except NoResultFound:
            return None

    def get_user(self, user_id):
        try:
            user = self.session.query(models.User).filter_by(id=user_id).one()
        except NoResultFound:
            return None

        return user
