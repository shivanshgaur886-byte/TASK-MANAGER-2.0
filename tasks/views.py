from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Task
from .forms import RegisterForm, TaskForm


# Home / Dashboard
@login_required(login_url='login')
def home(request):

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(
                request,
                'Task added successfully!'
            )
            return redirect('home')
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = TaskForm()

    query = request.GET.get('q')

    tasks = Task.objects.filter(user=request.user)

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    total_tasks = tasks.count()

    completed_tasks = tasks.filter(
        status='Completed'
    ).count()

    pending_tasks = tasks.filter(
        status='Pending'
    ).count()

    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'form': form,
    }

    return render(
        request,
        'home.html',
        context
    )


# Register Page
def register_page(request):

    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                'Account Created Successfully!'
            )

            return redirect('home')

    context = {
        'form': form
    }

    return render(
        request,
        'register.html',
        context
    )


# Login Page
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


def login_page(request):

    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm()

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            return redirect('home')

        else:
            messages.error(
                request,
                'Invalid Username or Password'
            )

    context = {
        'form': form
    }

    return render(
        request,
        'login.html',
        context
    )


# Logout
def logout_page(request):
    logout(request)
    return redirect('login')


# Add Task
@login_required(login_url='login')
def add_task(request):

    form = TaskForm()

    if request.method == 'POST':

        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            return redirect('home')

    context = {
        'form': form
    }

    return render(
        request,
        'add_task.html',
        context
    )


# Edit Task
@login_required(login_url='login')
def edit_task(request, pk):

    task = get_object_or_404(
        Task,
        id=pk,
        user=request.user
    )

    form = TaskForm(instance=task)

    if request.method == 'POST':

        form = TaskForm(
            request.POST,
            instance=task
        )

        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form
    }

    return render(
        request,
        'edit.html',
        context
    )


# Delete Task
@login_required(login_url='login')
def delete_task(request, pk):

    task = get_object_or_404(
        Task,
        id=pk,
        user=request.user
    )

    task.delete()

    return redirect('home')