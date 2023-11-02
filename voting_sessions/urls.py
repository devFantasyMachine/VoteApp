from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "voting_sessions"

urlpatterns = [

    path("", views.VotingSessionListApiView.as_view(), name="voting-sessions"),
    path("/<str:id>", views.VotingSessionUpdateDestroyApiView.as_view(),
         name="one-voting-sessions"),

    path("/<str:session_id>/positions", views.MemberPositionListApiView.as_view(),
         name="positions-voting-sessions"),

    path("/<str:session_id>/positions/<str:position_id>", views.MemberPositionUpdateDestroyRetrieveApiView.as_view(),
         name="one-positions-voting-sessions"),

    path("/<str:session_id>/subscriptions", views.UserVotingSessionSubscriptionListApiView.as_view(),
         name="positions-voting-sessions"),

    path("/<str:session_id>/subscriptions/change",
         views.UserVotingSessionSubscriptionUpdateDestroyRetrieveApiView.as_view(),
         name="one-positions-voting-sessions"),

    path("/<str:session_id>/candidates",
         views.MemberCandidateListApiView.as_view(),
         name="candidate-positions-voting-sessions"),

    path("/<str:session_id>/candidates/change",
         views.MemberCandidateUpdateDestroyRetrieveApiView.as_view(),
         name="candidate-positions-voting-sessions"),


    path("/<str:session_id>/positions/<str:position_id>/candidates/<str:candidate_id>",
         views.VoteListApiView.as_view(),
         name="votes-voting-sessions"),

]


