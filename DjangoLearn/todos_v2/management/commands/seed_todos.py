from django.core.management.base import BaseCommand

from DjangoLearn.todos_v2.models import Todo

SEED_DATA = [
    {"title": "Buy groceries", "description": "Milk, eggs, bread", "completed": False},
    {"title": "Read Django docs", "description": "Focus on ORM chapter", "completed": True},
    {"title": "Write tests", "description": "Cover all service functions", "completed": False},
    {"title": "Deploy to production", "description": "Use gunicorn + nginx", "completed": False},
    {"title": "Code review", "description": "Review PR #42", "completed": True},
]


class Command(BaseCommand):
    help = "Seed the database with sample todos"

    def handle(self, *args, **kwargs):
        Todo.objects.all().delete()
        todos = [Todo(**data) for data in SEED_DATA]
        Todo.objects.bulk_create(todos)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(todos)} todos"))
