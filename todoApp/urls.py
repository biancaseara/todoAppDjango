from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('todo/', views.todo, name='todo'),
    path('edit_task/<int:srno>', views.edit_task, name='edit_task'),
    path('delete/<int:srno>', views.delete, name='delete'),
    path('signout', views.signout, name='signout'),
]
