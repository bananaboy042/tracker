from django.urls import path
from .views import tracker, habbit_add, habbit_execute

urlpatterns = [
    path('tracker/', tracker, name="tracker"),
    path('add/', habbit_add, name="habbitadd"),
    path('execut_habbit/<int:habbit_id>/', habbit_execute, name='habbit_execut')
    ]