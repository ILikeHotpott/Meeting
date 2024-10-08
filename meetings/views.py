from rest_framework import generics, permissions
from meetings.models import Meeting, MeetingParticipant
from .serializers import MeetingSerializer, MeetingParticipantSerializer


class CreateMeetingView(generics.CreateAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


class JoinMeetingView(generics.CreateAPIView):
    serializer_class = MeetingParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
