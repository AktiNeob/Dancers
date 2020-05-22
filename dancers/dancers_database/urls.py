from django.urls import path
from .views import DancersView, DancerView


urlpatterns = [
    path('dancers/', DancersView.as_view()),
    path('dancer/<uuid:uuid>', DancerView.as_view()),
   
]

