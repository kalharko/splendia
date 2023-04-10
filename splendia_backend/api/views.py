from django.http import JsonResponse
from rest_framework import status

from api.models.game_manager import GameManager

def start_game(request):
    GameManager.objects.all().delete()
    game_manager = GameManager.objects.create_game_manager(2)
    game_manager.save()
    return JsonResponse(status = status.HTTP_OK)