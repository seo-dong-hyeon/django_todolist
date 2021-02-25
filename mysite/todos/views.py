from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Todo
from .form import TodoForm
from django.utils import timezone


def index(request):
    todos = Todo.objects.order_by('-created_at')
    context = {'todos': todos}
    return render(request, 'todos/todos.html', context)


def detail(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    context = {'todo': todo}
    return render(request, 'todos/todo_detail.html', context)


@login_required(login_url='user:login')
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.created_at = timezone.now()
            todo.author = request.user
            todo.save()
            return redirect('todos:index')
    else:
        form = TodoForm()
    context = {'form': form}

    return render(request, 'todos/todo_form.html', context)
