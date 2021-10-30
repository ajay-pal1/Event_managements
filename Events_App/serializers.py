from rest_framework import serializers
from . models import Event,EventJoined
from django.contrib.auth.models import User


class CreatorDetail(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ('username',)

class EventSerializer(serializers.ModelSerializer):
    creator=CreatorDetail(read_only = True)

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["creator"]= user
        return super().create(validated_data)

    class Meta:
        model=Event
        fields = "__all__"

class JoinedEventDetail(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields = "__all__"
        
class JoinedSerializer(serializers.ModelSerializer):
    user_profile=CreatorDetail(read_only = True)

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user_profile"]= user
        return super().create(validated_data)

    class Meta:
        model=EventJoined
        fields = "__all__"