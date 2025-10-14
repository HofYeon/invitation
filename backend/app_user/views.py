from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.middleware import csrf

class CookieLoginView(APIView):
    authentication_classes = []  # 로그인은 비인증
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=400)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        resp = Response({"username": user.username}, status=200)
        # HttpOnly 쿠키 설정 (프론트/백 분리: SameSite=None, Secure)
        cookie_opts = dict(
            httponly=True, secure=True, samesite="None", path="/",
        )
        resp.set_cookie("access", access_token, max_age=600, **cookie_opts)
        resp.set_cookie("refresh", refresh_token, max_age=7*24*3600, **cookie_opts)

        # CSRF 쿠키도 같이 발급(React가 헤더에 실어 보냄)
        resp.set_cookie("csrftoken", csrf.get_token(request), secure=True, samesite="None", path="/")
        return resp

class CookieRefreshView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        refresh = request.COOKIES.get("refresh")
        if not refresh:
            return Response({"detail": "No refresh cookie"}, status=401)
        try:
            token = RefreshToken(refresh)
            access = str(token.access_token)
        except Exception:
            return Response({"detail": "Invalid refresh"}, status=401)

        resp = Response(status=200)
        resp.set_cookie("access", access, max_age=600, httponly=True, secure=True, samesite="None", path="/")
        return resp

class LogoutView(APIView):
    def post(self, request):
        resp = Response(status=204)
        # 쿠키 제거
        for name in ["access", "refresh", "csrftoken"]:
            resp.delete_cookie(name, path="/")
        return resp
    


class CardCreateView():
    authentication_classes = []  # 로그인은 비인증
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=400)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        resp = Response({"username": user.username}, status=200)
        # HttpOnly 쿠키 설정 (프론트/백 분리: SameSite=None, Secure)
        cookie_opts = dict(
            httponly=True, secure=True, samesite="None", path="/",
        )
        resp.set_cookie("access", access_token, max_age=600, **cookie_opts)
        resp.set_cookie("refresh", refresh_token, max_age=7*24*3600, **cookie_opts)

        # CSRF 쿠키도 같이 발급(React가 헤더에 실어 보냄)
        resp.set_cookie("csrftoken", csrf.get_token(request), secure=True, samesite="None", path="/")
        return resp