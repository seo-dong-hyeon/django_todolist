from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
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


@login_required(login_url='user:login')
def todo_modify(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.user != todo.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('todos:detail', todo_id=todo.id)

    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.author = request.user
            todo.modify_date = timezone.now()  # 수정일시 저장
            todo.save()
            return redirect('todos:detail', todo_id=todo.id)
    else:
        form = TodoForm(instance=todo)
    context = {'form': form}
    return render(request, 'todos/todo_form.html', context)


@login_required(login_url='user:login')
def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.user != todo.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('todos:detail', todo_id=todo.id)
    todo.delete()
    return redirect('todos:index')