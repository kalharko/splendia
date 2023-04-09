from django.http import JsonResponse
from rest_framework import status

def start_game(request):
    return JsonResponse(status = status.HTTP_OK)