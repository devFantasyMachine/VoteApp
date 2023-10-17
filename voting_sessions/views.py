from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from voting_sessions.models import VotingSession, MemberPosition, UserVotingSessionSubscription, MemberCandidate, Vote
from voting_sessions.serializers import VotingSessionSerializer, VotingSessionModificationSerializer, \
    MemberPositionSerializer, UserVotingSessionSubscriptionSerializer, MemberCandidateSerializer, VoteSerializer


class MobileResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class VotingSessionListApiView(ListAPIView, CreateAPIView):
    """
        APIView for gospel entity
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = VotingSessionSerializer
    pagination_class = LargeResultsSetPagination
    queryset = VotingSession.objects.all()

    # 2. Create
    def post(self, request, *args, **kwargs):
        """
            Create one gospel entity
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        data = {**request.data, "creator": request.user}
        entity = VotingSession.objects.create(**data)
        entity.save()

        serializer = VotingSessionSerializer(entity)

        if serializer is not None:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)



class VotingSessionUpdateDestroyApiView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    """
        APIView for gospel entity
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = VotingSessionSerializer

    def get_object(self):

        try:
            return VotingSession.objects.get(id=self.kwargs['id'])
        except Exception:
            return None

    # 2. Update
    def put(self, request, *args, **kwargs):

        session = self.get_object()

        if session is None:
            return Response({'msg': "NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serializer = VotingSessionModificationSerializer(instance=session, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):

        session = self.get_object()
        if session is None:
            return Response({'msg': "NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)

        session.delete()
        return Response(status=status.HTTP_200_OK)


class MemberPositionListApiView(ListAPIView, CreateAPIView):
    """
        APIView for gospel entity
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = MemberPositionSerializer

    def get_queryset(self):

        voting_session_id = self.kwargs["session_id"]
        try:
            session = VotingSession.objects.get(id=voting_session_id)
            return MemberPosition.objects.filter(session=session)
        except Exception:
            return None

    # 2. Create
    def post(self, request, *args, **kwargs):

        voting_session_id = self.kwargs["session_id"]
        try:
            session = VotingSession.objects.get(id=voting_session_id)
        except Exception:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        if session.user.id != request.user.id:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        data = {**request.data, "session": session}
        entity = MemberPosition.objects.create(**data)
        entity.save()

        serializer = MemberPositionSerializer(entity)

        if serializer is not None:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)


class MemberPositionUpdateDestroyRetrieveApiView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    """
        APIView for gospel entity
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = MemberPositionSerializer

    def get_object(self):

        voting_session_id = self.kwargs["session_id"]
        position_id = self.kwargs["position_id"]
        try:
            session = VotingSession.objects.get(id=voting_session_id)
            return MemberPosition.objects.get(session=session.id, id=position_id)
        except Exception:
            return None

    # 2. Create
    def put(self, request, *args, **kwargs):

        if request.user.is_staff is False:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        position = self.get_object()

        if position is None:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        serializer = MemberPositionSerializer(instance=position, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):

        if request.user.is_staff is False:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        position = self.get_object()

        if position is None:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        position.delete()
        return Response(status=status.HTTP_200_OK)


class UserVotingSessionSubscriptionListApiView(ListAPIView, CreateAPIView):
    """
        APIView for gospel entity
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserVotingSessionSubscriptionSerializer

    def get_queryset(self):

        voting_session_id = self.kwargs["session_id"]
        try:
            session = VotingSession.objects.get(id=voting_session_id)
            return UserVotingSessionSubscription.objects.filter(session=session, is_locked=False)
        except Exception:
            return None

    # 2. Create
    def post(self, request, *args, **kwargs):

        voting_session_id = self.kwargs["session_id"]
        try:
            session = VotingSession.objects.get(id=voting_session_id)
        except Exception:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        data = {"user": request.user, "session": session}
        entity = UserVotingSessionSubscription.objects.create(**data)
        entity.save()

        serializer = UserVotingSessionSubscriptionSerializer(entity)

        if serializer is not None:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)


class UserVotingSessionSubscriptionUpdateDestroyRetrieveApiView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    """
        APIView for gospel entity
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserVotingSessionSubscriptionSerializer

    def get_object(self):

        voting_session_id = self.kwargs["session_id"]
        try:
            session = VotingSession.objects.get(id=voting_session_id)
            return UserVotingSessionSubscription.objects.get(session=session.id, user=self.request.user.id, is_locked=False )
        except Exception:
            return None

    # 2. Create
    def put(self, request, *args, **kwargs):

        if request.user.is_staff is False:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        user_session = self.get_object()

        if user_session is None:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserVotingSessionSubscriptionSerializer(instance=user_session, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):

        user_session = self.get_object()

        if user_session is None or user_session.user.id != request.user.id:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        user_session.delete()
        return Response(status=status.HTTP_200_OK)


class MemberCandidateListApiView(ListAPIView, CreateAPIView):
    """
        APIView for gospel entity
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = MemberCandidateSerializer

    def get_queryset(self):

        voting_session_id = self.kwargs["session_id"]
        voting_position_id = self.kwargs["position_id"]
        try:
            session = VotingSession.objects.get(id=voting_session_id)
            position = MemberPosition.objects.get(session=session, id=voting_position_id)
            return MemberCandidate.objects.filter(position=position)
        except Exception:
            return None

    # 2. Create
    def post(self, request, *args, **kwargs):

        voting_session_id = self.kwargs["session_id"]
        voting_position_id = self.kwargs["position_id"]
        try:
            session = VotingSession.objects.get(id=voting_session_id)
            position = MemberPosition.objects.get(session=voting_session_id, id=voting_position_id)
            subscription = UserVotingSessionSubscription.objects.get(session=voting_session_id, user=self.request.user.id,
                                                                     is_locked=False, is_active=True)

        except Exception:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        old_candidates = MemberCandidate.objects.filter(session=session.id, user=request.user.id)
        if old_candidates is not None and len(old_candidates) > 0:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        if subscription is None:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        if position.status != "OPEN":
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        data = {"user": request.user, "position": position}
        entity = MemberCandidate.objects.create(**data)
        entity.save()

        serializer = MemberCandidateSerializer(entity)

        if serializer is not None:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)


class MemberCandidateUpdateDestroyRetrieveApiView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    """
        APIView for gospel entity
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = MemberCandidateSerializer

    def get_queryset(self):

        voting_session_id = self.kwargs["session_id"]
        try:
            session = VotingSession.objects.get(id=voting_session_id)
            return MemberCandidate.objects.get(session=session.id, user=self.request.user.id)
        except Exception:
            return None

    # 2. Create
    def put(self, request, *args, **kwargs):

        candidate = self.get_object()

        if request.user.id != candidate.user:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        serializer = MemberCandidateSerializer(instance=candidate, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):

        candidate = self.get_object()

        if candidate is None or candidate.user.id != request.user.id:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        candidate.delete()
        return Response(status=status.HTTP_200_OK)


class VoteListApiView(ListAPIView, CreateAPIView):
    """
        APIView for gospel entity
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = VoteSerializer

    def get_queryset(self):

        voting_candidate_id = self.kwargs["candidate_id"]
        voting_position_id = self.kwargs["position_id"]
        try:
            return Vote.objects.filter(candidate=voting_candidate_id, position=voting_position_id)
        except Exception:
            return None

    # 2. Create
    def post(self, request, *args, **kwargs):

        candidate_id = self.kwargs["candidate_id"]
        voting_session_id = self.kwargs["session_id"]
        voting_position_id = self.kwargs["position_id"]
        try:
            position = MemberPosition.objects.get(session=voting_session_id, id=voting_position_id)
            subscription = UserVotingSessionSubscription.objects.get(session=voting_session_id, user=self.request.user.id,
                                                                     is_locked=False, is_active=True)
        except Exception:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        if subscription is None:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        candidate = MemberCandidate.objects.get(id=candidate_id, position=voting_position_id)

        if candidate is not None and candidate.user.id == request.user.id:
            return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)

        data = {"user": request.user, "position": position, "candidate": candidate}
        entity = Vote.objects.create(**data)
        entity.save()

        serializer = VoteSerializer(entity)

        if serializer is not None:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'msg': "something was wrong"}, status=status.HTTP_403_FORBIDDEN)




