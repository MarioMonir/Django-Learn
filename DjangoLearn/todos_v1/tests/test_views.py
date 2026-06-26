import json

from django.test import Client, TestCase
from django.urls import reverse

from DjangoLearn.todos_v1.models import Todo


class TodoViewTests(TestCase):
    test_payload = {
        "title": "Create Test title",
        "description": "Create Test description",
    }

    test_not_found_id = 999999

    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(
            title=self.test_payload["title"],
            description=self.test_payload["description"],
        )

    def test_list_todo(self):
        response = self.client.get(reverse("todo_list_create"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        todo = data[0]
        self.assertIsInstance(todo["id"], int)
        self.assertIsInstance(todo["description"], str)
        self.assertIsInstance(todo["completed"], bool)
        self.assertIsInstance(todo["created_at"], str)
        self.assertIsInstance(todo["updated_at"], str)
        self.assertEqual(todo["title"], self.todo.title)
        self.assertEqual(todo["description"], self.todo.description)
        self.assertEqual(todo["completed"], self.todo.completed)

    def test_create_todo(self):
        test_create_payload = {"title": "test create payload"}
        response = self.client.post(
            reverse("todo_list_create"),
            data=json.dumps(test_create_payload),
            content_type="application/json",
        )
        todo = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(todo["title"], test_create_payload["title"])
        self.assertIsInstance(todo["created_at"], str)
        self.assertIsInstance(todo["updated_at"], str)

    def test_get_todo(self):
        response = self.client.get(
            reverse("todo_detail", kwargs={"id": self.todo.id}),
        )
        self.assertEqual(response.status_code, 200)
        todo = json.loads(response.content)
        self.assertEqual(todo["title"], self.todo.title)
        self.assertEqual(todo["description"], self.todo.description)
        self.assertEqual(todo["completed"], self.todo.completed)

    def test_get_not_found_todo(self):
        response = self.client.get(
            reverse("todo_detail", kwargs={"id": self.test_not_found_id}),
        )
        self.assertEqual(response.status_code, 404)

    def test_update_todo(self):
        updated_todo = {
            "title": "Updated Title",
            "description": "Updated description",
            "completed": True,
        }
        response = self.client.put(
            reverse("todo_detail", kwargs={"id": self.todo.id}),
            data=json.dumps(updated_todo),
        )

        todo = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(todo["title"], updated_todo["title"])
        self.assertEqual(todo["description"], updated_todo["description"])
        self.assertEqual(todo["completed"], updated_todo["completed"])

    def test_update_not_found_todo(self):
        updated_todo = {
            "title": "Updated Title",
            "description": "Updated description",
            "completed": True,
        }
        response = self.client.put(
            reverse("todo_detail", kwargs={"id": self.test_not_found_id}),
            data=json.dumps(updated_todo),
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_todo(self):
        response = self.client.delete(
            reverse("todo_detail", kwargs={"id": self.todo.id}),
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_unfound_todo(self):
        response = self.client.delete(
            reverse("todo_detail", kwargs={"id": self.test_not_found_id}),
        )
        self.assertEqual(response.status_code, 404)
        self.test_get_not_found_todo()
