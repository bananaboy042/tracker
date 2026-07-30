from django.urls import path
from .views import tracker, habbit_add, habbit_execute, edit_habit, delete_habit

urlpatterns = [
    path('tracker/', tracker, name="tracker"),
    path('add/', habbit_add, name="habbitadd"),
    path('execut_habbit/<int:habbit_id>/', habbit_execute, name='habbit_execut'),
    path('edithabit/<int:habbit_id>/', edit_habit, name='habit_edit'),
    path('habit_del/<int:habbit_id>/', delete_habit, name='habit_del')
    ]