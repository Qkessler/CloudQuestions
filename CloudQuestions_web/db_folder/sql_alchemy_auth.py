from sqlalchemy.orm.exc import NoResultFound
from models.user import User
from db_folder.session_factory import create_session


class SQLAlchemyUserBackend(object):
    supports_anonymous_user = True
    supports_inactive_user = True

    def __init__(self):
        self.session = create_session()

    def authenticate(self, username=None, password=None):
        try:
            user = self.session.query(
                User).filter_by(username=username).one()
            if user.check_password(password):
                return user
        except NoResultFound:
            return None

    def get_user(self, user_id):
        try:
            user = self.session.query(User).filter_by(id=user_id).one()
        except NoResultFound:
            return None

        return user
