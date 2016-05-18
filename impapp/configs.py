__author__ = 'Abdul'
from settings import LOCAL

URL = 'https://api.instagram.com/oauth/access_token'
CLIENT_ID = '970bf284ea4648189378dc2c95a394b8'
CLIENT_SECRET = '27c2fff562004767b64ab23518a4a8ee'
REDIRECT_URI = 'http://localhost:8000/redirect_insta' if LOCAL else 'http://79.143.180.194/redirect_insta'

