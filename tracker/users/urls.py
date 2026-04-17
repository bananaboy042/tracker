from django.urls import path

from .views import register, verify_code

urlpatterns = [
    path('register/', register, name="register"),
    path('verifycode/<int:user_id>/', verify_code, name='verifycode')



]