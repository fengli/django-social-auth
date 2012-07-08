from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages

from social_auth import __version__ as version
from social_auth.utils import setting
from app.forms import RegistrationFormSimple


def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return HttpResponseRedirect('done')
    else:
        return render_to_response('home.html', {'version': version},
                                  RequestContext(request))


@login_required
def done(request):
    """Login complete view, displays user data"""
    ctx = {
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    return render_to_response('home.html', ctx, RequestContext(request))


def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'version': version,
                                             'messages': messages},
                              RequestContext(request))

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')

def social_registration (request,
                   template_name="registration_form.html"):
  """
  part of the socail registration pipeline. Return a form for fill
  if it's a new user.
  """
  from social_auth.utils import setting
  name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')

  if request.method == 'POST':
    form = RegistrationFormSimple (data=request.POST, files=request.FILES)
    if form.is_valid():
      request.session['saved_username'] = request.POST['username']
      request.session['saved_email'] = request.POST['email']
      request.session['saved_password'] = request.POST['password1']
      backend=request.session[name]['backend']
      return redirect('socialauth_complete', backend=backend)
  else:
    social_info = {}
    try:
      sf=request.session[name]['kwargs']
      social_info['username']=sf['details']['username']
      social_info['email']=sf['details']['email']
    except KeyError,e: print e
    print 'social_info',social_info
    form = RegistrationFormSimple (initial=social_info)

  context = RequestContext(request)
  return render_to_response(template_name,
                            {'form': form},
                            context_instance=context)
