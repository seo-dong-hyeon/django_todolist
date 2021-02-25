from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Todo, Comment
from .form import TodoForm, CommentForm
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


@login_required(login_url='user:login')
def comment_create(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.created_at = timezone.now()
            comment.todo = todo
            comment.save()
            return redirect('todos:detail', todo_id=todo.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'todos/comment_form.html', context)


@login_required(login_url='user:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('todos:detail', todo_id=comment.todo.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.updated_at = timezone.now()
            comment.save()
            return redirect('todos:detail', todo_id=comment.todo.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'todos/comment_form.html', context)


@login_required(login_url='user:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('todos:detail', todo_id=comment.todo.id)
    else:
        comment.delete()
    return redirect('todos:detail', todo_id=comment.todo.id)