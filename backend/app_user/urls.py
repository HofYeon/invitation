from django.urls import path
from .views import CookieLoginView, CookieRefreshView, LogoutView, CardCreateView

urlpatterns = [
    path("auth/cookie-login/", CookieLoginView.as_view()),
    path("auth/cookie-refresh/", CookieRefreshView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    path("card/create/", CardCreateView.as_view()),
]