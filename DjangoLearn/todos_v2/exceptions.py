from rest_framework.exceptions import NotFound


class TodoNotFound(NotFound):
    def __init__(self, todo_id):
        super().__init__(f"Todo with id {todo_id} not found ")
