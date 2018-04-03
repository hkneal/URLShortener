from __future__ import unicode_literals

from django.db import models
import string, random

nick_nameSet = set()

def genterateNick_Name():
    #Generates a random 8 character nickname from 0-9,A-Z, and a-z character set
    nick_name = ""
    for num in range(0,8):
        nick_name += random.choice(string.digits + string.letters)
    return nick_name

class UrlManager(models.Manager):
    nick_nameSet = set()
    nick_name = ""
    def shortenURL(self, postData):
        full_URL = postData['full_URL']
        print "inside of URLMANAGER - full_URL:", full_URL
        valid = False
        while(not valid):
            #if we don't generate a unique nickname, regenerate
            nick_name = genterateNick_Name()
            if(not nick_name in nick_nameSet):
                nick_nameSet.add(nick_name)
                valid = True
                break
        urlMessage = "Your shortened URL is " + nick_name
        print "Your shortened URL is " + nick_name
        url = UrlName.objects.create(
            full_URL = full_URL,
            nick_name = nick_name
            )
        return {
            'url':url,
            'message': urlMessage
            }

    def retrieve(self, postData):
        nickname = postData['nick_name']
        try:
            url = UrlName.objects.get(nick_name = nickname)
            full_URL = url.full_URL
            message = "Your Full URL is " + full_URL
            return {
                'url':url,
                'message' : message
                }
        except:
            message = "Please try a different nickname, the nickname entered was invalid"
            return {
                'errorMessage' : message
                }



# Create your models here.
class UrlName(models.Model):
    full_URL = models.CharField(max_length=2083, default="Enter in the full URL")
    nick_name = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UrlManager()
