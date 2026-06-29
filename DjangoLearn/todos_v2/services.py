import logging

from DjangoLearn.todos_v2.models import Todo
from DjangoLearn.todos_v2.exceptions import TodoNotFound

logger = logging.getLogger(__name__)


def list_todos():
    return Todo.objects.all()


def get_todo(todo_id: int) -> Todo:
    try:
        return Todo.objects.get(pk=todo_id)
    except Todo.DoesNotExist:
        raise TodoNotFound(todo_id)


def create_todo(data) -> Todo:
    logger.info("Creating todo with title: %s", data.get("title"))
    return Todo.objects.create(**data)


def update_todo(todo_id: int, data) -> Todo:
    todo = get_todo(todo_id)
    for field, value in data.items():
        setattr(todo, field, value)
    todo.save()
    logger.info("Updated todo %s", todo_id)
    return todo


def delete_todo(todo_id: int) -> None:
    todo = get_todo(todo_id)
    todo.delete()
    logger.info("Deleted todo %s", todo_id)
