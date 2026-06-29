from django.test import TestCase

from DjangoLearn.todos_v2.exceptions import TodoNotFound
from DjangoLearn.todos_v2.models import Todo
from DjangoLearn.todos_v2.services import (
    create_todo,
    delete_todo,
    get_todo,
    list_todos,
    update_todo,
)


class TodoServiceTest(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(
            title="Test Title",
            description="Test Description",
        )

    def test_list_todos(self):
        result = list_todos()
        self.assertEqual(result.count(), 1)

    def test_create_todo(self):
        result = create_todo({"title": "New Todo", "description": "New Description"})
        self.assertIsInstance(result, Todo)
        self.assertEqual(result.title, "New Todo")
        self.assertEqual(result.description, "New Description")
        self.assertFalse(result.completed)

    def test_get_todo(self):
        result = get_todo(self.todo.id)
        self.assertIsInstance(result, Todo)
        self.assertEqual(result.id, self.todo.id)
        self.assertEqual(result.title, self.todo.title)

    def test_get_todo_not_found(self):
        with self.assertRaises(TodoNotFound):
            get_todo(9999)

    def test_update_todo(self):
        result = update_todo(self.todo.id, {"title": "Updated", "description": "Updated Desc"})
        self.assertIsInstance(result, Todo)
        self.assertEqual(result.title, "Updated")
        self.assertEqual(result.description, "Updated Desc")

    def test_update_todo_partial(self):
        result = update_todo(self.todo.id, {"title": "Only Title Updated"})
        self.assertEqual(result.title, "Only Title Updated")
        self.assertEqual(result.description, self.todo.description)

    def test_update_todo_not_found(self):
        with self.assertRaises(TodoNotFound):
            update_todo(9999, {"title": "Nope"})

    def test_delete_todo(self):
        delete_todo(self.todo.id)
        self.assertEqual(Todo.objects.count(), 0)

    def test_delete_todo_not_found(self):
        with self.assertRaises(TodoNotFound):
            delete_todo(9999)
