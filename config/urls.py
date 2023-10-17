from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/accounts", include("accounts.urls", namespace="users")),
    path("api/voting-sessions", include("voting_sessions.urls", namespace="voting-sessions")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
