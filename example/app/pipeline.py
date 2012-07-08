from social_auth.utils import setting
from social_auth.models import User
from social_auth.backends.pipeline import USERNAME, USERNAME_MAX_LENGTH, \
                                          warn_setting
from social_auth.signals import socialauth_not_registered, \
                                socialauth_registered, \
                                pre_update

from django.http import HttpResponseRedirect
from app.forms import RegistrationFormSimple
from django.core.urlresolvers import reverse

def redirect_to_form (*args, **kwargs):
    if not kwargs['request'].session.get('saved_username') and \
            not kwargs.get('user'):
        return HttpResponseRedirect (reverse ('accounts_social_registration'))

def restore_user_info (request, user=None, *args, **kwargs):
    if user:
        username = user.username
        email = user.email
        return {'username':username, 'email':email, 'user': user, 'password':None}

    username = request.session.get('saved_username')
    email = request.session.get('saved_email')
    password = request.session.get('saved_password')
    print username,email,password
    return {'username':username,'email':email,'password':password}

def create_user (backend, details, response, uid, username,
                 email, password, user = None, *args, **kwargs):
    if user:
        return {'user':user}
    if not username or not email or not password:
        return None

    warn_setting ('SOCIAL_AUTH_CREATE_USERS', 'create_user')

    if not setting('SOCIAL_AUTH_CREATE_USERS', True):
        # Send signal for cases where tracking failed registering is useful.
        socialauth_not_registered.send(sender=backend.__class__,
                                       uid=uid,
                                       response=response,
                                       details=details)
        return None

    return {
        'user': User.objects.create_user(username=username, email=email, password=password),
        'is_new': True
    }

