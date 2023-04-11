from django.urls import path 
from . import views 
 
urlpatterns = [ 
    path(r'api/start_game', views.start_game),
]
