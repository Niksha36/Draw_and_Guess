from django.urls import path
from .views import ScoreUpdate


urlpatterns = [
    path('score/<int:user_id>/update', ScoreUpdate.as_view(), name='user-score'),
]
