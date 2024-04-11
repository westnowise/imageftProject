from django.shortcuts import render, redirect
from . import forms
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect('login')  # 회원가입 성공 시 로그인 페이지로 이동
    else:
        form = forms.SignUpForm()
    return render(request, 'account/signup.html', {'form': form})