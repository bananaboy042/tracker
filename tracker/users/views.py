import json

from django.contrib.auth import login, logout, authenticate
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.utils import timezone

from .models import User
from .utils import has_russian_letters, validate_and_format_phone, generation_code, send_message_by_phone_number, \
    phone_masked


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
        user = User.objects.create_user(username=login, phone=number, password=password1,
                                        verification_code=verification_code, code_sent_at=timezone.now())

        send_message_by_phone_number(user)

        return redirect('verifycode', user_id=user.id)

def verify_code(request, user_id):
    user = User.objects.get(id=user_id)
    context = {'phone_number': phone_masked(user.phone), 'user_id': user.id}
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

def logout_user(request):
    logout(request)
    return redirect('main')


def newcode(request, user_id):
    verification_code = generation_code()
    user = User.objects.get(id=user_id)
    user.verification_code = verification_code
    user.save()
    send_message_by_phone_number(user)
    return JsonResponse({'success': True})


def login_user(request):
    if request.method == "GET":
        username = request.GET.get('username', '')
        return render(request, 'loginuser.html', {'login': username})
    elif request.method == "POST":
        login_user = request.POST.get('username')
        password = request.POST.get('password')
        error = False
        context = {}
        if has_russian_letters(login_user):
            error = True
            context['login_error'] = 'Логин не должен содержать русских букв'
        else:
            user = authenticate(request, username=login_user, password=password)
            if user is not None:
                login(request, user)
                return redirect('tracker')
            else:
                if User.objects.filter(username=login_user).exists():
                    error = True
                    context['password_error'] = 'Неверный пароль'
                else:
                    error = True
                    context['login_error'] = 'Такого пользователя не существует'

        if error:
            context['login'] = login_user

        return render(request, 'loginuser.html', context=context)


def res_password(request):
    if request.method == 'GET':
        return render(request, 'reset_pass.html')
    elif request.method == 'POST':
        data = json.loads(request.body)
        user_login = data.get('username')

        if User.objects.filter(username=user_login).exists():
            verification_code = generation_code()
            user = User.objects.get(username=user_login)
            user.verification_code = verification_code
            user.save()
            send_message_by_phone_number(user)
            return JsonResponse({
                'success': True,
                'phone_masked': phone_masked(user.phone)})
        else:
            return JsonResponse({
                'success': False,
                'error': 'Такого пользователя не существует'
            }, status=400)


def verify_reset_code(request):
    data = json.loads(request.body)
    username = data.get("username")
    code = data.get("code")

    # 1. Получаем пользователя по username
    user = User.objects.get(username=username.strip())

    if code == user.verification_code:
        # То тут проверка пароля прошла
        success = True
    else:
        success = False

    return JsonResponse({'success': success})


def res_pas(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("new_password")
    confirm_pas = data.get("confirm_pas")

    if password != confirm_pas:
        success = False

    else:

        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        success = True

    return JsonResponse({'success': success})

