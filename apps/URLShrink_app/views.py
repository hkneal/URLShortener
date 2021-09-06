from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from .serializers import UrlNameSerializer
from .models import UrlName
from .forms import shorten_URL_form, expand_URL_form

#Get hostname for API functions
from django.contrib.sites.shortcuts import get_current_site

# Main view for browser
def index(req):
    context = {
        'shorten_URL_form' : shorten_URL_form(),
        'expand_URL_form' : expand_URL_form()
    }
    return render(req, 'URLShrink_app/index.html', context)

# Get a shortened URL
def shortenURL(req):
    form = shorten_URL_form(req.POST)
    if form.is_valid():
        postData = {
            'full_URL' : form.cleaned_data['full_URL']
            }
        url = UrlName.objects.shortenURL(postData)
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
    print("Inside of Return Expanded###")
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

#API Views

#POST a new URL
class CreateView(generics.CreateAPIView):
    #queryset = UrlName.objects.all()
    serializer_class = UrlNameSerializer

    def create(self, request, *args, **kwargs):
        current_site = get_current_site(request)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"Fail": "Make sure a fully qualified URL is sent"})

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)
        return Response({"Success": "Your shortened URL is: " + current_site.name + "/" + serializer.data['nick_name'] }, headers=headers)

    def perform_create(self, serilizer):
        serilizer.save()

#Get all URLs
class GetView(generics.ListAPIView):
    queryset = UrlName.objects.all()
    serializer_class = UrlNameSerializer

#Get full URL from a nick_name
class GetNickNameView(generics.ListAPIView):
    serializer_class = UrlNameSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        nick_name = self.kwargs['nick_name']
        queryset = self.model.objects.filter(nick_name = nick_name)
        return queryset

# class DeleteNickNameView(generics.DestroyAPIView):
#     serializer_class = UrlNameSerializer
#     model = serializer_class.Meta.model
#
#     def get_queryset(self):
#         nick_name = self.kwargs['nick_name']
#         queryset = self.model.objects.filter(nick_name = nick_name)
#         return queryset
