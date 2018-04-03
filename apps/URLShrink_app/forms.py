from django import forms
from .models import UrlName
from django.core.exceptions import ValidationError
import re

URL_PROPER = re.compile(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

def validateURL(urlInput):
    if URL_PROPER.match(urlInput):
        return True
    else:
        return False

def validateNickName(nicknameInput):
    return any(char.isalnum() for char in nicknameInput)

class shorten_URL_form(forms.Form):
    full_URL = forms.CharField(label='Paste in your full URL', max_length=2083, min_length=8, required=True)

    def clean_full_URL(self):
        #validate the input url for a proper structure
        thisfull_URL = self.cleaned_data['full_URL']
        if len(thisfull_URL) > 20838:
            raise ValidationError('Full URL must be less than 2083 characters/numbers')
        if(not validateURL(thisfull_URL)):
            raise ValidationError('You must enter in a proper URL, eg. https://www.linkedin.com/in/hiram-neal')
        return thisfull_URL

class expand_URL_form(forms.Form):
    nick_name = forms.CharField(label='Enter your last 8 characters of your shortened URL:', max_length=8, min_length=8, required=True)

    def clean_nick_name(self):
        #validate the input url for a proper structure
        thisnick_name = self.cleaned_data['nick_name']
        if not len(thisnick_name) == 8:
            raise ValidationError('Shortend name input must be 8 characters/numbers')
        if(not validateNickName(thisnick_name)):
            raise ValidationError('You must enter only the last 8 characters of your shortened URL.')
        return thisnick_name
