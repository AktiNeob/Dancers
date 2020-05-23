from django.urls import path
from .views import Competition, Competitions


urlpatterns = [
    path('compititions/', BaseCreateNewCompetition.as_view()),
    path('compitition/<uuid:uuid>', Competition.as_view()),
   
]
