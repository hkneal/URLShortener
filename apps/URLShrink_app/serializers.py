from rest_framework import serializers
from .models import UrlName
import string, random, re

class UrlNameSerializer(serializers.ModelSerializer):
    #serialize to map URLName to JSON

    URL_PROPER = re.compile(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

    def validateURL(self, urlInput):
        if self.URL_PROPER.match(urlInput):
            return True
        else:
            return False


    full_URL = serializers.CharField(label='Paste in your full URL', max_length=2083, min_length=8, required=True)

    class Meta:
        model = UrlName
        fields = ('full_URL', 'nick_name', 'created_at', 'updated_at')
        read_only_fields = ('nick_name', 'created_at', 'updated_at')
        extra_kwargs = {}

    def validate_full_URL(self, full_URL):
        #Check for proper URL
        if len(full_URL) > 2083:
            raise serializers.ValidationError('Full URL must be less than 2083 characters/numbers')
        if(not self.validateURL(full_URL)):
            raise serializers.ValidationError('You must enter in a proper URL, eg. https://www.linkedin.com/in/hiram-neal')

        return full_URL
