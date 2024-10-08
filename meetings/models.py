from django.db import models
from django.conf import settings
import shortuuid


class Meeting(models.Model):
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hosted_meetings'
    )
    title = models.CharField(max_length=12, unique=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    url = models.URLField(max_length=255, blank=True, null=True)

    def _generate_short_uuid(self):
        return shortuuid.ShortUUID().random(length=12)

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self._generate_short_uuid()
        if not self.url:
            self.url = f"http://localhost:8000/{self.title}"
        super(Meeting, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class MeetingParticipant(models.Model):
    ROLE_CHOICES = [
        ('host', 'Host'),
        ('participant', 'Participant')
    ]

    STATUS_CHOICES = [
        ('invited', 'Invited'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined')
    ]

    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name='participants'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='meetings'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='invited')

    class Meta:
        unique_together = ('meeting', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.meeting.title}"
