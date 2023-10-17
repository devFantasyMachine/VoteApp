from django.contrib.auth.hashers import check_password
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from voting_sessions.models import VotingSession, MemberPosition, UserVotingSessionSubscription, MemberCandidate


class VotingSessionSerializer(serializers.ModelSerializer):
    """
        Serializer class to serialize User model.
    """

    class Meta:
        model = VotingSession
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class VotingSessionModificationSerializer(serializers.ModelSerializer):
    """
        Serializer class to serialize User model.
    """

    class Meta:
        model = VotingSession
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'creator']


class MemberPositionSerializer(serializers.ModelSerializer):
    """
        Serializer class to serialize User model.
    """

    class Meta:
        model = MemberPosition
        fields = '__all__'
        read_only_fields = ['created_at', 'session']


class UserVotingSessionSubscriptionSerializer(serializers.ModelSerializer):
    """
        Serializer class to serialize User model.
    """

    class Meta:
        model = UserVotingSessionSubscription
        fields = '__all__'
        read_only_fields = ['created_at', 'session', 'user']


class MemberCandidateSerializer(serializers.ModelSerializer):
    """
        Serializer class to serialize User model.
    """

    class Meta:
        model = MemberCandidate
        fields = '__all__'
        read_only_fields = ['posted_at', 'position', 'user']



