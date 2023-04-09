from django.apps import AppConfig
from model.game_manager import GameManager;


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    game_manager = GameManager()
    
    def __init__(self) -> None:
        print(self.game_manager, "test")
