from django.urls import path
from . import views

app_name = 'todos'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:todo_id>/', views.detail, name='detail'),
    path('create', views.todo_create, name='todo_create'),
    path('modify/<int:todo_id>/', views.todo_modify, name='todo_modify'),
    path('delete/<int:todo_id>/', views.todo_delete, name='todo_delete'),
    path('comment/create/<int:todo_id>/', views.comment_create, name='comment_create'),
    path('comment/modify/<int:comment_id>/', views.comment_modify, name='comment_modify'),
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
]