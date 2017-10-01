from rest_framework import serializers
from bori.models import News
from django.contrib.auth.models import User

class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ('url','name')

