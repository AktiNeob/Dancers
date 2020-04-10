from django.urls import path
from .views import DancersView, print_page,print_data, DancerView


urlpatterns = [
    path('test/', DancersView.as_view()),
    path('dancer/<uuid:uuid>', DancerView.as_view()),
    path('page/', print_page),
    path('ping/', print_data),
]

