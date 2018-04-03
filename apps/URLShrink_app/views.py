from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import UrlName
from .forms import shorten_URL_form, expand_URL_form

# Create your views here.
def index(req):
    context = {
        'shorten_URL_form' : shorten_URL_form(),
        'expand_URL_form' : expand_URL_form()
    }
    return render(req, 'URLShrink_app/index.html', context)

def shortenURL(req):
    form = shorten_URL_form(req.POST)
    if form.is_valid():
        postData = {
            'full_URL' : form.cleaned_data['full_URL']
            }
        url = UrlName.objects.shortenURL(postData)
        #print url['message']
        message = url['message']
        context = {
            'shorten_URL_form' : shorten_URL_form(),
            'expand_URL_form' : expand_URL_form(),
            'url' : url['url']
        }
        return render(req, 'URLShrink_app/index.html', context)
    else:
        context = {
            'shorten_URL_form' : shorten_URL_form(),
            'expand_URL_form' : expand_URL_form(),
            'errorMessage': "Improper URL, please enter the full URL, eg. https://www.linkedin.com"
        }
        return render(req, 'URLShrink_app/index.html', context)
        #return HttpResponse(message)

def expandURL(req, nick_name):
    #Get the db object of our nickname and pull the full URL then redirect to that url
    url = UrlName.objects.get(nick_name=nick_name)
    post = url.full_URL
    return redirect(post)

def returnExpanded(req):
    #Return the full url
    print "Inside of Return Expanded###"
    form = expand_URL_form(req.POST)
    if form.is_valid():
        postData = {
            'nick_name' : form.cleaned_data['nick_name']
            }
        originalUrl = UrlName.objects.retrieve(postData)
        if 'errorMessage' in originalUrl:
            context = {
                'shorten_URL_form' : shorten_URL_form(),
                'expand_URL_form' : expand_URL_form(),
                'errorMessageFull': originalUrl['errorMessage']
            }
            return render(req, 'URLShrink_app/index.html', context)
        else:
            #print url['message']
            message = originalUrl['message']
            context = {
                'shorten_URL_form' : shorten_URL_form(),
                'expand_URL_form' : expand_URL_form(),
                'originalUrl' : originalUrl['url']
            }
            return render(req, 'URLShrink_app/index.html', context)
    else:
        context = {
            'shorten_URL_form' : shorten_URL_form(),
            'expand_URL_form' : expand_URL_form(),
            'errorMessage': "Improper nickname, please only enter the last 8 characters."
        }
        return render(req, 'URLShrink_app/index.html', context)
