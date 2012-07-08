"""
Weibo OAuth support.

This contribution adds support for Weibo OAuth service. The settings
WEIBO_APP_ID and WEIBO_API_SECRET must be defined with the values
given by sina weibo application registration process.
"""
from django.conf import settings
from django.utils import simplejson

from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, USERNAME


# Weibo configuration
WEIBO_SERVER = 't.sina.com.cn'
WEIBO_API = 'api.%s' % WEIBO_SERVER
WEIBO_REQUEST_TOKEN_URL = 'http://%s/oauth/request_token' % WEIBO_API
WEIBO_AUTHORIZATION_URL = 'http://%s/oauth/authorize' % WEIBO_API
WEIBO_ACCESS_TOKEN_URL = 'http://%s/oauth/access_token' % WEIBO_API
WEIBO_CHECK_AUTH = 'http://%s/account/verify_credentials.json'%WEIBO_API

class WeiboBackend(OAuthBackend):
    """Weibo OAuth authentication backend"""
    name = 'weibo'
    # Default extra data to store
    EXTRA_DATA = [('id', 'id')]

    def get_user_details(self, response):
        """Return user details from Weibo account"""
        return {USERNAME: response.get('name'),
                'email': response.get('email',''),
                'first_name': response.get('screenName')}

class WeiboAuth(ConsumerBasedOAuth):
    """Weibo OAuth authentication mechanism"""
    AUTHORIZATION_URL = WEIBO_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = WEIBO_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = WEIBO_ACCESS_TOKEN_URL
    SERVER_URL = WEIBO_API
    AUTH_BACKEND = WeiboBackend
    SETTINGS_KEY_NAME = 'WEIBO_APP_ID'
    SETTINGS_SECRET_NAME = 'WEIBO_API_SECRET'

    def user_data(self, access_token):
        """Loads user data from service"""
        request = self.oauth_request(access_token, WEIBO_CHECK_AUTH)
        response = self.fetch_response(request)
        try:
            return simplejson.loads(response)
        except ValueError:
            return None

    @classmethod
    def enabled(cls):
        """Return backend enabled status by checking basic settings"""
        return all(hasattr(settings, name) for name in
                        ('WEIBO_APP_ID',
                         'WEIBO_API_SECRET'))


# Backend definition
BACKENDS = {
    'weibo': WeiboAuth,
}
