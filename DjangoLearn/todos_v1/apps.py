# This file is the app's identity card. Django uses it to register your app.

# AppConfig - base class Django provides for app configuration
# default_auto_field - tells Django what type to use for auto generated primary keys.
# name - the full python import path to your app. Must match exactly how it lives in the folder structure


from django.apps import AppConfig


class TodosV1Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "DjangoLearn.todos_v1"
