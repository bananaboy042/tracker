from django.urls import path

from .views import (register, verify_code, logout_user, newcode, login_user, res_password, verify_reset_code,
                    res_pas)

urlpatterns = [
    path('register/', register, name="register"),
    path('verifycode/<int:user_id>/', verify_code, name='verifycode'),
    path('logout/', logout_user, name="logout"),
    path('newverifycode/<int:user_id>/', newcode, name='newverifycode'),
    path('loginuser/', login_user, name='loginuser'),
    path('resetpassword/', res_password, name='res_password'),
    path('verify-reset-code/', verify_reset_code, name='verify_reset_code'),
    path('res_pas/', res_pas, name='res_pas')
]