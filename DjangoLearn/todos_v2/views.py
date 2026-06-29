import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request

from DjangoLearn.todos_v2.serializers import TodoCreateUpdateSerializer, TodoSerializer
from DjangoLearn.todos_v2.services import (
    create_todo,
    delete_todo,
    list_todos,
    get_todo,
    update_todo,
)

logger = logging.getLogger(__name__)


class TodoViewSet(ViewSet):
    def list(self, _: Request):
        todos = list_todos()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def retrieve(self, _: Request, pk: int):
        todo = get_todo(pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def create(self, request: Request):
        serializer = TodoCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        todo = create_todo(serializer.validated_data)
        return Response(TodoSerializer(todo).data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, pk: int):
        serializer = TodoCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        todo = update_todo(pk, serializer.validated_data)
        return Response(TodoSerializer(todo).data)

    def partial_update(self, request: Request, pk: int):
        serializer = TodoCreateUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        todo = update_todo(pk, serializer.validated_data)
        return Response(TodoSerializer(todo).data)

    def destroy(self, _: Request, pk: int):
        delete_todo(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
