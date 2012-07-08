"""
Douban OAuth support.

This contribution adds support for Douban OAuth service. The settings
DOUBAN_APP_ID and DOUBAN_API_SECRET must be defined with the values
given by Douban application registration process.
"""
from django.conf import settings
from django.utils import simplejson

from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, USERNAME


# Douban configuration
DOUBAN_SERVER = 'www.douban.com'
DOUBAN_API = '%s/service' % DOUBAN_SERVER
DOUBAN_REQUEST_TOKEN_URL = 'http://%s/auth/request_token' % DOUBAN_API
DOUBAN_AUTHORIZATION_URL = 'http://%s/auth/authorize' % DOUBAN_API
DOUBAN_ACCESS_TOKEN_URL = 'http://%s/auth/access_token' % DOUBAN_API
DOUBAN_CHECK_AUTH = 'http://api.douban.com/people/%40me'

class DoubanBackend(OAuthBackend):
    """Douban OAuth authentication backend"""
    name = 'douban'
    # Default extra data to store
    EXTRA_DATA = [('id', 'id')]

    def get_user_details(self, response):
        """Return user details from Douban account"""
        return {USERNAME: response.get('username'),
                'email': response.get('email',''),
                'first_name': response.get('title')}

class DoubanAuth(ConsumerBasedOAuth):
    """Douban OAuth authentication mechanism"""
    AUTHORIZATION_URL = DOUBAN_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = DOUBAN_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = DOUBAN_ACCESS_TOKEN_URL
    SERVER_URL = DOUBAN_API
    AUTH_BACKEND = DoubanBackend
    SETTINGS_KEY_NAME = 'DOUBAN_APP_ID'
    SETTINGS_SECRET_NAME = 'DOUBAN_API_SECRET'

    # Douban return xml format, here we just extract the information we need.
    # the ID, USERNAME, and TITLE
    def xml_to_dict (self, data):
        from BeautifulSoup import BeautifulStoneSoup as BS
        soup = BS(data)
        username = soup.find('db:uid').contents[0]
        uid = soup.find('id').contents[0].split('/')[-1]
        title = soup.find('title').contents[0]
        return {'id':uid, 'username':username,'title':title}

    def user_data(self, access_token):
        """Loads user data from service"""
        request = self.oauth_request(access_token, DOUBAN_CHECK_AUTH)
        response = self.fetch_response(request)
        try:
            return self.xml_to_dict (response)
        except ValueError:
            return None

    @classmethod
    def enabled(cls):
        """Return backend enabled status by checking basic settings"""
        return all(hasattr(settings, name) for name in
                        ('DOUBAN_APP_ID',
                         'DOUBAN_API_SECRET'))


# Backend definition
BACKENDS = {
    'douban': DoubanAuth,
}
