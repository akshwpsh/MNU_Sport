from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import LoginForm

class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')  # 로그인 후 이동할 페이지
            else:
                messages.error(request, "로그인 정보가 올바르지 않습니다.")
        return render(request, 'accounts/login.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')  # 로그아웃 후 이동할 페이지

