from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import Habbit


@login_required
def tracker(request):

    return render(request, 'tracker.html', context={'habits': Habbit.objects.filter(user=request.user)})

@login_required
def habbit_add(request):
    if request.method == "GET":

        return render(request,'habbitadd.html',)
    else:

        habbit_name = request.POST.get('name')
        description = request.POST.get('description')
        color = '#' + request.POST.get('color_hex_input', 'd9a5b3')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        frequency = request.POST.get('frequency_type')


        context = {
            'name': habbit_name,
            'description': description,
            'color': color,
            'start_date': start_date,
            'end_date': end_date,
            'frequency_type': frequency,
        }


        daily = {'type': frequency}
        if frequency == 'daily':
            daily_interval = request.POST.get('daily_interval', 1)
            daily['interval'] = int(daily_interval)
            context['daily_interval'] = daily_interval
        elif frequency == 'weekly':
            week_days = request.POST.getlist('week_days', [1])
            daily['days'] = [int(item) for item in week_days]
            context['week_days'] = week_days
        else:
            monthly_day = request.POST.get('monthly_day', 1)
            daily['day'] = int(monthly_day)
            context['monthly_day'] = monthly_day

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
        except Exception:
            context['error_message'] = 'Неверный формат даты. Используйте формат ГГГГ-ММ-ДД'
            return render(request, 'habbitadd.html', context=context)

        try:
            Habbit.objects.create(name=habbit_name, description=description, color=color,
                                  start_date=start_date, end_date=end_date, frequency=daily, user=request.user)
            return redirect('tracker')
        except ValidationError as e:
            context['error_message'] = e.messages[0]
            return render(request, 'habbitadd.html', context=context)

def habbit_execute(request, habbit_id):
    if request.method == 'POST':
        habbit = Habbit.objects.get(pk=habbit_id)
        last_executed = now().date()
        habbit.last_executed = last_executed
        habbit.count = habbit.count + 1
        habbit.save()
        return redirect('tracker')

def edit_habit(request, habbit_id):
    habit = Habbit.objects.get(pk=habbit_id)
    if request.method == 'GET':
        return render(request, 'habit_edit.html', context={'habit': habit})
    else:
        habit_name = request.POST.get('name')
        description = request.POST.get('description')
        habit.name = habit_name
        habit.description = description
        habit.save()
        return render(request, 'habit_edit.html', context={'habit': habit})


def delete_habit(request, habbit_id):
    if request.method == 'POST':
        Habbit.objects.get(pk=habbit_id).delete()
        return redirect('tracker')
