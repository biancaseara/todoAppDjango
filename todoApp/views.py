from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .models import Todo
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            my_user = User.objects.create_user(username=username, email=email, password=password)
            my_user.save()
            messages.success(request, 'Signup successful! You can now log in.')
            return redirect('login')
        except IntegrityError:
            messages.error(request, 'Username already taken. Please choose another one.')

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('todo')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'login.html')


@login_required(login_url='login')
def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        task = Todo(title=title, user=request.user)
        task.save()

        return redirect('todo')

    user_todos = Todo.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'user_todos': user_todos})


@login_required(login_url='login')
def edit_task(request, srno):
    task = get_object_or_404(Todo, srno=srno)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        task.title = title
        task.save()

        return redirect('todo')

    user_todos = Todo.objects.filter(user=request.user).order_by('-date')
    return render(request, 'edit_task.html', {'task': task, 'user_todos': user_todos})


@login_required(login_url='login')
def delete(request, srno):
    task = get_object_or_404(Todo, srno=srno)
    task.delete()

    return redirect('todo')


def signout(request):
    logout(request)
    return redirect('login')