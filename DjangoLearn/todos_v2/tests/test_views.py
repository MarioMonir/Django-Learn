from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from DjangoLearn.todos_v2.models import Todo


class TodoViewSetTest(APITestCase):
    def setUp(self):
        self.todo = Todo.objects.create(
            title="Test Title",
            description="Test Description",
        )

    def test_list_todos(self):
        response = self.client.get(reverse("todo-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.todo.title)

    def test_create_todo(self):
        payload = {"title": "New Todo", "description": "New Description"}
        response = self.client.post(reverse("todo-list"), data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])
        self.assertEqual(response.data["description"], payload["description"])
        self.assertFalse(response.data["completed"])

    def test_create_todo_missing_title(self):
        response = self.client.post(reverse("todo-list"), data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_todo(self):
        response = self.client.get(reverse("todo-detail", kwargs={"pk": self.todo.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.todo.title)
        self.assertEqual(response.data["description"], self.todo.description)

    def test_retrieve_todo_not_found(self):
        response = self.client.get(reverse("todo-detail", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_todo(self):
        payload = {"title": "Updated Title", "description": "Updated Desc", "completed": True}
        response = self.client.put(
            reverse("todo-detail", kwargs={"pk": self.todo.id}),
            data=payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], payload["title"])
        self.assertEqual(response.data["completed"], True)

    def test_update_todo_not_found(self):
        payload = {"title": "Updated Title", "description": "Updated Desc"}
        response = self.client.put(
            reverse("todo-detail", kwargs={"pk": 9999}),
            data=payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_todo(self):
        response = self.client.patch(
            reverse("todo-detail", kwargs={"pk": self.todo.id}),
            data={"completed": True},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["completed"])
        self.assertEqual(response.data["title"], self.todo.title)

    def test_delete_todo(self):
        response = self.client.delete(reverse("todo-detail", kwargs={"pk": self.todo.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)

    def test_delete_todo_not_found(self):
        response = self.client.delete(reverse("todo-detail", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
