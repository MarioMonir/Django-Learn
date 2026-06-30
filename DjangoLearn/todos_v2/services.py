import logging

from django.contrib.auth import get_user_model

from DjangoLearn.todos_v2.exceptions import TodoNotFound
from DjangoLearn.todos_v2.models import Todo

logger = logging.getLogger(__name__)

User = get_user_model()


def list_todos(user):
    return Todo.objects.filter(user=user)


def get_todo(todo_id: int, user) -> Todo:
    try:
        return Todo.objects.get(pk=todo_id, user=user)
    except Todo.DoesNotExist:
        raise TodoNotFound(todo_id)


def create_todo(data, user) -> Todo:
    logger.info("Creating todo for user %s", user.email)
    return Todo.objects.create(user=user, **data)


def update_todo(todo_id: int, data, user) -> Todo:
    todo = get_todo(todo_id, user)
    for field, value in data.items():
        setattr(todo, field, value)
    todo.save()
    logger.info("Updated todo %s", todo_id)
    return todo


def delete_todo(todo_id: int, user) -> None:
    todo = get_todo(todo_id, user)
    todo.delete()
    logger.info("Deleted todo %s", todo_id)
