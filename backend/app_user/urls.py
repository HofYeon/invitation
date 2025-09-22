from django.urls import path
from auth.views import CookieLoginView, CookieRefreshView, LogoutView

urlpatterns += [
    path("auth/cookie-login/", CookieLoginView.as_view()),
    path("auth/cookie-refresh/", CookieRefreshView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
]