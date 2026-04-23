
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, HttpResponse
from django.utils import timezone

from .models import User
from .utils import has_russian_letters, validate_and_format_phone, generation_code, send_message_by_phone_number


def register(request):
    if request.method == 'GET':
        return render(request, "register.html")
    else:
        login = request.POST.get('username')
        user_number = request.POST.get('phone_number')
        error = False
        context = {}
        if has_russian_letters(login):
            error = True
            context['login_error'] = 'Логин не должен содержать русских букв'

        number = validate_and_format_phone(user_number)
        if not number:
            error = True
            context['phone_error'] = 'Неверный формат номера телефона'

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            error = True
            context['password_error'] = 'Пароли не совпадают'

        db_login = User.objects.filter(username=login)
        db_number = User.objects.filter(phone=number)
        if db_login or db_number:
            error = True
            context['duplicate_error'] = 'Такой логин или номер телефона уже существует'

        if error:
            context['login'] = login
            context['number'] = user_number
            return render(request, 'register.html', context)

        verification_code = generation_code()
        user = User.objects.create_user(username=login, phone=number,
                                        verification_code=verification_code, code_sent_at=timezone.now())

        send_message_by_phone_number(user)



        """
        редирект на строницу  в котором пользователь будет вводить код из смс, в котором будет кнопка отправить код повторно
        ВАЖНО! В УРЛЕ ПЕРЕДАТЬ ID пользователя
        return redirect(f'/verify-code/{user.id}/')
        
        мы 
        
        Если пользователь нажал отправить код повторно
        1) Мыц должны сгенерировать новый код
        2) Обновить запись о коде в БД
        3) отправить ему новую СМС
        
        """

        return redirect('verifycode', user_id=user.id)

def verify_code(request, user_id):
    user = User.objects.get(id=user_id)
    context = {'phone_number': user.phone}
    if request.method == "GET":
        return render(request, "verifycode.html", context)
    elif request.method == "POST":
        verifycode = request.POST.get("code")
        if verifycode == user.verification_code:
            login(request, user)

        #     тут должна быть авторизация
            return redirect('tracker')
        else:
            context["verify_error"] = 'Неверный код. Введите правильно, либо отправьте смс заново'
            return render(request, "verifycode.html", context)

def tracker(request):
    return render(request, 'tracker.html')



def logout_user(request):
    logout(request)
    return redirect('main')

