from __future__ import unicode_literals

from django.db import models
import string, random

nick_nameSet = set()

def generateNick_Name():
    #Generates a random 8 character nickname from 0-9,A-Z, and a-z character set
    valid = False
    while(not valid):
        nick_name = ""
        for num in range(0,8):
            nick_name += random.choice(string.digits + string.ascii_letters)
        if(not nick_name in nick_nameSet):
            nick_nameSet.add(nick_name)
            valid = True
            break
    return nick_name

class UrlManager(models.Manager):
    nick_nameSet = set()
    nick_name = ""

    def shortenURL(self, postData):
        full_URL = postData['full_URL']
        #print "inside of URLMANAGER - full_URL:", full_URL
        nick_name = generateNick_Name()
        urlMessage = "Your shortened URL is " + nick_name
        #print "Your shortened URL is " + nick_name
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
    nick_name = models.CharField(primary_key = True, max_length=8, default = generateNick_Name)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UrlManager()
