from rest_framework import serializers

from app.models import AccessToken

class CoreTokenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccessToken
        fields = ('access_token','expire_in')