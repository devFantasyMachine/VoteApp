from django.http import HttpResponse
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer, UpdateUserSerializer, UserRegistrationSerializer, UserLoginSerializer


class UserList(generics.ListAPIView):
    """
        An endpoint for the client to get all user info
    """
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    """
    An endpoint for the client to create a new User by email field
    """

    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request,  *args, **kwargs):
        email = request.data["mat"]

        user = User.objects.filter(email=email)
        if user is not None and len(user) > 0:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN, content="user already exists")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        data["is_new_user"] = True
        return Response(data, status=status.HTTP_201_CREATED)



class UserLoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing users using their email and password.
    """

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = UserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data

        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        data["is_new_user"] = False

        return Response(data, status=status.HTTP_200_OK)


class UserLogoutAPIView(GenericAPIView):
    """
        An endpoint to logout users.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(RetrieveUpdateAPIView):
    """
        Get, Update user information
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return User.objects.get(id=self.kwargs["id"])

    def put(self, request, *args, **kwargs):

        try:
            user = User.objects.get(id=kwargs["id"])
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND, content="user not found")

        if user.id != request.user.id:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN, content="forbidden")

        serializer = UpdateUserSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer = UserSerializer(user, data=serializer.data, partial=True)
        return Response(data=serializer.data)


class PseudoAvailableAPIView(RetrieveAPIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        pseudo = kwargs["pseudo"]

        try:
            User.objects.get(pseudo=pseudo)
            return False
        except User.DoesNotExist:
            return True
