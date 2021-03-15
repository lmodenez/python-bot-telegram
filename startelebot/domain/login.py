from datetime import date
from startelebot.infrastructure.dbservice import DbService

class Login():

    def __init__(self):
        self.db_service = DbService()

    def user_is_logged(self, user):
        try:
            result = self.db_service.get_user_login_data(user.id)
            expiration_date = result.get("EXPIRATION_DATE")
            if  date.today() <= expiration_date.date():
                return True
            return False
        except:
            return False

    def verify_user_password(self, user, password):
        try:
            result = self.db_service.get_user_login_data(user.id)
            if password == result.get("PASSWORD"):
                self.db_service.increase_expiration_date(user.id, 1)
                return True
            return False
        except:
            pass