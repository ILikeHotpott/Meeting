from rest_framework import serializers
from .models import Meeting, MeetingParticipant


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'


class MeetingParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingParticipant
        fields = '__all__'
