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

class shorten_URL_form(forms.Form):
    full_URL = forms.CharField(label='Paste in your full URL', max_length=2083, min_length=8, required=True)

    def clean_full_URL(self):
        #validate the input url for a proper structure
        thisfull_URL = self.cleaned_data['full_URL']
        if(not validateURL(thisfull_URL)):
            raise ValidationError('You must enter in a proper URL, eg. https://www.linkedin.com/in/hiram-neal')
        return thisfull_URL

class expand_URL_form(forms.Form):
    nick_name = forms.CharField(label='Enter your last 8 characters of your shortened URL:', max_length=8, min_length=8, required=True)
