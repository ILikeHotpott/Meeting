from django.contrib import admin
from .models import Meeting, MeetingParticipant

admin.site.register(Meeting)
admin.site.register(MeetingParticipant)
