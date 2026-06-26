from django.urls import path
from . import views


urlpatterns = [
    path("", views.todo_list_create, name="todo_list_create"),
    path("<int:id>/", views.todo_detail, name="todo_detail"),
    path("page/", views.todo_page, name="todo_page"),
    path("page/<int:id>/update/", views.todo_update_view, name="todo_update_view"),
    path("page/<int:id>/delete/", views.todo_delete_view, name="todo_delete_view"),
    path("page/<int:id>/toggle/", views.todo_toggle_view, name="todo_toggle_view"),
]
