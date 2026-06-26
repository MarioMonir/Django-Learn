class TodoNotFound(Exception):
    def __init__(self, todo_id: int):
        super().__init__(f"Todo with {todo_id} not found")

    pass
