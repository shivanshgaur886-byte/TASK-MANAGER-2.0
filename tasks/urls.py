from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'register/',
        views.register_page,
        name='register'
    ),

    path(
        'login/',
        views.login_page,
        name='login'
    ),

    path(
        'logout/',
        views.logout_page,
        name='logout'
    ),

    path(
        'add-task/',
        views.add_task,
        name='add_task'
    ),

    path(
        'edit-task/<int:pk>/',
        views.edit_task,
        name='edit_task'
    ),

    path(
        'delete-task/<int:pk>/',
        views.delete_task,
        name='delete_task'
    ),
]