from asyncio import Condition
from rest_framework import generics, permissions
from meetings.models import Meeting, MeetingParticipant
from .serializers import MeetingSerializer, MeetingParticipantSerializer


class CreateMeetingView(generics.CreateAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user, Condition=1)


class JoinMeetingView(generics.CreateAPIView):
    serializer_class = MeetingParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        meeting = serializer.validated_data['meeting']

        if meeting.condition == 1:
            serializer.save(user=self.request.user)



class TerminateMeetingView(generics.UpdateAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Meeting.objects.filter(host=self.request.user)

    def update(self, request, *args, **kwargs):
        meeting = self.get_object()
        
        meeting.condition = 0 
        meeting.save()

