import json

from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from DjangoLearn.todos_v1.exceptions import TodoNotFound
from DjangoLearn.todos_v1.services import (
    create_todo,
    delete_todo,
    get_todo,
    list_todo,
    update_todo,
)


# --- Template Views ---

def todo_page(request):
    editing = None
    edit_id = request.GET.get("edit")

    if request.method == "POST":
        create_todo(request.POST)
        return redirect("todo_page")

    if edit_id:
        try:
            editing = get_todo(int(edit_id))
        except TodoNotFound:
            pass

    return render(request, "todos_v1/todo_page.html", {
        "todos": list_todo(),
        "editing": editing,
    })


def todo_update_view(request, id):
    if request.method == "POST":
        try:
            update_todo(id, request.POST)
        except TodoNotFound:
            pass
    return redirect("todo_page")


def todo_delete_view(request, id):
    try:
        delete_todo(id)
    except TodoNotFound:
        pass
    return redirect("todo_page")


def todo_toggle_view(request, id):
    try:
        todo = get_todo(id)
        update_todo(id, {"completed": not todo["completed"]})
    except TodoNotFound:
        pass
    return redirect("todo_page")


# --- API Views ---

@csrf_exempt
@require_http_methods(["GET", "POST"])
def todo_list_create(request: HttpRequest):
    if request.method == "GET":
        todos = list_todo()
        return JsonResponse(todos, status=200, safe=False)

    if request.method == "POST":
        body = json.loads(request.body)
        todo = create_todo(body)
        return JsonResponse(todo, status=201)

    return JsonResponse({"error": "method not allowed"}, status=405)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def todo_detail(request: HttpRequest, id: int):
    try:
        if request.method == "GET":
            todo = get_todo(id)
            return JsonResponse(todo, status=200)

        if request.method == "PUT":
            body = json.loads(request.body)
            todo = update_todo(id, body)
            return JsonResponse(todo, status=200)

        if request.method == "DELETE":
            delete_todo(id)
            return HttpResponse(status=204)

        return JsonResponse({"error": "Method not allowed"}, status=405)

    except TodoNotFound as e:
        return JsonResponse({"error": str(e)}, status=404)
