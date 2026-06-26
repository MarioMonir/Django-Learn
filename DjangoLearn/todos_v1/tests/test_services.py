from django.test import TestCase

from DjangoLearn.todos_v1.exceptions import TodoNotFound
from DjangoLearn.todos_v1.models import Todo
from DjangoLearn.todos_v1.services import (
    create_todo,
    delete_todo,
    get_todo,
    update_todo,
)


class TodoServiceTest(TestCase):
    test_payload = {
        "title": "Create Test title",
        "description": "Create Test descriptionn",
    }

    def setUp(self):
        self.todo = Todo.objects.create(
            title=self.test_payload["title"],
            description=self.test_payload["description"],
        )

    def test_create_todo(self):
        result = create_todo(self.test_payload)
        self.assertEqual(result["title"], self.test_payload["title"])
        self.assertEqual(result["description"], self.test_payload["description"])
        self.assertEqual(result["completed"], False)

    def test_get_todo(self):
        result = get_todo(self.todo.id)
        self.assertEqual(result["id"], self.todo.id)
        self.assertEqual(result["title"], self.todo.title)
        self.assertEqual(result["description"], self.test_payload["description"])
        self.assertEqual(result["completed"], False)

    def test_get_todo_not_found(self):
        with self.assertRaises(TodoNotFound):
            get_todo(9999)

    def test_update_todo(self):
        updated_payload = {
            "title": "Updated Title",
            "description": "Updated Description",
        }
        result = update_todo(self.todo.id, updated_payload)
        self.assertEqual(result["title"], updated_payload["title"])
        self.assertEqual(result["description"], updated_payload["description"])

    def test_update_todo_partial(self):
        updated_payload = {"title": "Only Update Title"}
        result = update_todo(self.todo.id, updated_payload)
        self.assertEqual(result["title"], updated_payload["title"])
        self.assertEqual(result["description"], self.todo.description)

    def test_update_todo_not_found(self):
        updated_payload = {"title": "Update Title"}
        with self.assertRaises(TodoNotFound):
            update_todo(9999, updated_payload)

    def test_delete_todo(self):
        delete_todo(self.todo.id)
        self.assertEqual(Todo.objects.count(), 0)

    def test_delete_todo_not_found(self):
        with self.assertRaises(TodoNotFound):
            delete_todo(9999)
