from django.urls import path
from . import views

app_name = 'todos'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:todo_id>/', views.detail, name='detail'),
    path('create', views.todo_create, name='todo_create'),
    path('modify/<int:todo_id>/', views.todo_modify, name='todo_modify'),
]