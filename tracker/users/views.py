from django.shortcuts import render
from .utils import has_russian_letters, validate_and_format_phone


def register(request):
    if request.method == 'GET':
        return render(request, "register.html")
    else:
        login = request.POST.get('username')
        user_number = request.POST.get('phone_number')
        if has_russian_letters(login):
            return render(request, "register.html", context={
                'login_error': 'Логин не должен содержать русских букв',
                'login': login,
                'number': user_number
                                                             })

        number = validate_and_format_phone(user_number)
        if not number:
            return render(request, "register.html", context={
                'phone_error': 'Неверный формат номера телефона',
                'login': login,
                'number':user_number
                                                             })
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return render(request, "register.html", context={
                'password_error': 'Пароли не совпадают',
                'login':login,
                'number': user_number
                                } )
        print(login,number,password1,password2)
        return render(request, "register.html")