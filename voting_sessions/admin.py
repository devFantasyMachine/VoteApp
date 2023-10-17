from django.contrib import admin

from voting_sessions.models import VotingSession, Vote, MemberPosition, MemberCandidate, UserVotingSessionSubscription

admin.site.register(VotingSession)
admin.site.register(MemberPosition)
admin.site.register(MemberCandidate)
admin.site.register(UserVotingSessionSubscription)
admin.site.register(Vote)
