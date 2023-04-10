from django.http import JsonResponse
from rest_framework import status

from api.models.game_manager import GameManager

def start_game(request):
    print(GameManager.objects.all().count())
    game_manager = GameManager.objects.get_game_manager()
    game_manager.start_new_game(2)
    return JsonResponse(data = "", safe=False, status = status.HTTP_200_OK)