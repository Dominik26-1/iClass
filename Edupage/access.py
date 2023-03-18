import os

from edupage_api import Edupage
from edupage_api.exceptions import BadCredentialsException
from urllib3.exceptions import ReadTimeoutError

edupage = Edupage()
edupage_username = os.environ.get('EDUPAGE_USER')
edupage_password = os.environ.get('EDUPAGE_PASSWORD')

try:
    edupage.login(edupage_username, edupage_password, subdomain="gta")
except BadCredentialsException:
    print("Wrong username or password for edupage login!")
except ReadTimeoutError:
    print("Poor or no connection to internet!")
