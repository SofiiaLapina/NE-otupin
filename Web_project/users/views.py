from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Реєстрація успішна! Ласкаво просимо!")
            return redirect('home')
        else:
            messages.error(request, "Помилка у формі. Будь ласка, перевірте введені дані.")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Перенаправляємо на головну сторінку
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})