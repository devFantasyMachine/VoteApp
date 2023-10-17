import uuid

from django.db import models


# Create your models here.
from accounts.models import User

VotingSessionStatus = [
    ("PLANNED", "PLANNED"),
    ("IN_PROGRESS", "IN_PROGRESS"),
    ("FINISHED", "FINISHED")
]

MemberPositionStatus = [
    ("OPEN", "OPEN"),
    ("CLOSED", "CLOSED"),
    ("VOTED", "VOTED")
]


class VotingSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    label = models.CharField(max_length=255, blank=False, null=False, unique=True)
    description = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(default="PLANNED", choices=VotingSessionStatus, max_length=25, blank=False, null=False,)

    def __str__(self):
        return "{} ({})".format(self.label, self.description)


class UserVotingSessionSubscription(models.Model):
    session = models.ForeignKey(VotingSession, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    is_active = models.BooleanField(null=False, default=True)
    is_locked = models.BooleanField(null=False, default=False)

    locked_at = models.DateTimeField(null=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} --> user: {}".format(self.session, self.user)


class MemberPosition(models.Model):
    session = models.ForeignKey(VotingSession, null=False, on_delete=models.CASCADE)
    label = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default="OPEN", choices=MemberPositionStatus, max_length=25, blank=False, null=False, )

    def __str__(self):
        return "{}".format(self.label)


class MemberCandidate(models.Model):
    position = models.ForeignKey(MemberPosition, null=False, on_delete=models.CASCADE)
    session = models.ForeignKey(VotingSession, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    reason = models.TextField(null=False, blank=False)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} user: {}".format(self.position, self.user)


class Vote(models.Model):
    candidate = models.ForeignKey(MemberCandidate, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    value = models.SmallIntegerField(null=False, default=1)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} user: {}".format(self.candidate, self.user)

