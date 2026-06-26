from django.http import HttpRequest, JsonResponse


def ping(_: HttpRequest):
    return JsonResponse({"message": "pong"})
