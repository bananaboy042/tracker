from django.urls import path
from .views import tracker


urlpatterns = [
    path('tracker/', tracker, name="tracker"),

    ]