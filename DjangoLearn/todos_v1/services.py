from DjangoLearn.todos_v1.exceptions import TodoNotFound
from DjangoLearn.todos_v1.models import Todo


def list_todo():
    todos = Todo.objects.all()
    # data = list(todos.values())
    data = [
        {
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed,
            "created_at": todo.created_at.isoformat(),
            "updated_at": todo.updated_at.isoformat(),
        }
        for todo in todos
    ]

    return data


def create_todo(todo_payload):
    todo = Todo.objects.create(
        title=todo_payload.get("title"),
        description=todo_payload.get("description", ""),
    )

    return {
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "created_at": todo.created_at.isoformat(),
        "updated_at": todo.updated_at.isoformat(),
    }


def get_todo(todo_id: int):
    try:
        todo = Todo.objects.get(id=todo_id)
        return {
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed,
            "created_at": todo.created_at.isoformat(),
            "updated_at": todo.updated_at.isoformat(),
        }
    except Todo.DoesNotExist:
        raise TodoNotFound(todo_id)


def update_todo(todo_id, todo_payload):
    try:
        todo = Todo.objects.get(id=todo_id)
        todo.title = todo_payload.get("title", todo.title)
        todo.description = todo_payload.get("description", todo.description)
        todo.completed = todo_payload.get("completed", todo.completed)
        todo.save()

        return {
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed,
            "created_at": todo.created_at.isoformat(),
            "updated_at": todo.updated_at.isoformat(),
        }
    except Todo.DoesNotExist:
        raise TodoNotFound(todo_id)


def delete_todo(todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        todo.delete()
    except Todo.DoesNotExist:
        raise TodoNotFound(todo_id)
