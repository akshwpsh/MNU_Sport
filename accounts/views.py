from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import *
from django.contrib.auth.models import User

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
                return redirect('/records/admin/')  # 로그인 후 이동할 페이지
            else:
                messages.error(request, "로그인 정보가 올바르지 않습니다.")
        return render(request, 'accounts/login.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')  # 로그아웃 후 이동할 페이지

class RegisterView(View):
    def get(self, request):
        if request.user.is_superuser:
            return render(request, 'accounts/register.html')
        else:
            return redirect('/')

    def post(self, request):
        # 슈퍼 어드민 계정일 경우에만
        if request.user.is_superuser:
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                return redirect('/accounts/user_list/')

        return render(request, 'accounts/register.html')

class UserListView(View):
    def get(self, request):
        if request.user.is_superuser:
            users = User.objects.all()
            print(users)
            return render(request, 'accounts/user_list.html', {'users': users})
        else:
            return redirect('/')

class UserDeleteView(View):
    def get(self, request, user_id):
        if request.user.is_superuser:
            user = User.objects.get(id=user_id)
            user.delete()
            return redirect('user_list')
        else:
            return redirect('/')