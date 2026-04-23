from django.urls import path

from .views import register, verify_code, tracker, logout_user

urlpatterns = [
    path('register/', register, name="register"),
    path('verifycode/<int:user_id>/', verify_code, name='verifycode'),
    path('tracker/', tracker, name="tracker"),
    path('logout', logout_user, name="logout")



]