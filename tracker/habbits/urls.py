from django.urls import path
from .views import tracker, habbit_add

urlpatterns = [
    path('tracker/', tracker, name="tracker"),
    path('add/', habbit_add, name="habbitadd")
    ]