from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "users"

urlpatterns = [
    path("/register", views.UserRegistrationAPIView.as_view(), name="create-user-by-email"),
    path("/login", views.UserLoginAPIView.as_view(), name="login-user"),
    path("/available/<str:pseudo>", views.PseudoAvailableAPIView.as_view(), name="pseudo available"),

    path("/<str:id>", views.UserAPIView.as_view(), name="update"),

    path("", views.UserList.as_view(), name="get-all"),
    path("/token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("/logout", views.UserLogoutAPIView.as_view(), name="logout-user"),
    path("/info", views.UserAPIView.as_view(), name="user-info"),
]
