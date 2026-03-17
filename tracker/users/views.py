from django.shortcuts import render
from .utils import has_russian_letters


def register(request):
    if request.method == 'GET':
        return render(request, "register.html")
    else:
        login = request.POST.get('username')
        if has_russian_letters(login):
            return render(request, "register.html", context={'login_error': 'Логин не должен содержать русских букв'})
        number = request.POST.get('phone_number')
        if not validate_phone_number(number):
            return render(request, "register.html", context={'phone_error': 'Неверный формат номера телефона'})

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(login,number,password1,password2)
        return render(request, "register.html")