import os

from edupage_api import Edupage
from edupage_api.exceptions import BadCredentialsException
from urllib3.exceptions import ReadTimeoutError

from App.logger import logger

edupage_username = os.environ.get('EDUPAGE_USER')
edupage_password = os.environ.get('EDUPAGE_PASSWORD')
domain = "gta"


class EdupageAccount:
    def __init__(self, username, password, domain):
        self.edupage = Edupage()
        self.username = username
        self.password = password
        self.domain = domain

    def get_edupage(self):
        return self.edupage

    def login(self):
        try:
            self.edupage.login(self.username, self.password, self.domain)
        except BadCredentialsException:
            logger.warning("Wrong username or password for edupage login!")
        except ReadTimeoutError:
            logger.warning("Poor or no connection to internet! for edupage login!")


edupage_account = EdupageAccount(edupage_username, edupage_password, domain)
