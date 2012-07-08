#-*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegistrationFormSimple(forms.Form):
    """
    Form for registering a new user account.

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """
    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(),
                                help_text=_(u"用户名只能由字母,数字和下划线组成."),
                                error_messages={ 'invalid': _(u"用户名只能由字母,数字和下划线组成."),'required':_(u"请输入你的用户名") },
                                label=_(u"用户名"),)
    email = forms.EmailField(widget=forms.TextInput(),
                             label=_(u"邮箱地址"),
                             help_text=_(u"请放心，我们不会将你的邮箱地址公布或者用于商业用途."),
                             error_messages={'invalid': _(u"请输入有效的邮箱地址."), 'required': _(u"请输入邮箱地址.") })
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                error_messages={'required': _(u"请输入密码.")},
                                label=_(u"设置密码"))
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(u"抱歉，这个用户名已经被注册过了，换一个吧"))
    
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_(u"这个邮箱已经注册过了，请选择另外的邮箱进行注册."))
        return self.cleaned_data['email']
