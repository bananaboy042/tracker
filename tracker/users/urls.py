from django.urls import path

from .views import register, verify_code, tracker, logout_user, newcode

urlpatterns = [
    path('register/', register, name="register"),
    path('verifycode/<int:user_id>/', verify_code, name='verifycode'),
    path('tracker/', tracker, name="tracker"),
    path('logout', logout_user, name="logout"),
    path('newverifycode/<int:user_id>/', newcode, name='newverifycode')



]