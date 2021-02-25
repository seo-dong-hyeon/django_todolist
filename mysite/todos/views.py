from django.shortcuts import render
from django.http import HttpResponse
from .models import Todo


def index(request):
    todos = Todo.objects.all()
    context = {'todos': todos}
    return render(request, 'todos/todos.html', context)


def detail(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    context = {'todo': todo}
    return render(request, 'todos/todo_detail.html', context)
