from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render

from .models import Color, Habbit


@login_required
def tracker(request):
    return render(request, 'tracker.html')

@login_required
def habbit_add(request):
    if request.method == "GET":
        colors = Color.objects.all()
        return render(request,'habbitadd.html', context={'colors':colors})
    else:
        colors = Color.objects.all()
        habbit_name = request.POST.get('name')
        description = request.POST.get('description')
        color_id = request.POST.get('color')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        frequency = request.POST.get('frequency_type')

        daily_interval = 1
        week_days = []
        monthly_day = 1

        daily = {'type': frequency}
        if frequency == 'daily':
            daily_interval = request.POST.get('daily_interval', 1)
            daily['interval'] = int(daily_interval)
        elif frequency == 'weekly':
            week_days = request.POST.getlist('week_days', [1])
            daily['days'] = [int(item) for item in week_days]
        else:
            monthly_day = request.POST.get('monthly_day', 1)
            daily['day'] = int(monthly_day)

        context = {'colors': colors}


        context = {
            'colors': colors,
            'name': habbit_name,
            'description': description,
            'selected_color': int(color_id) if color_id else None,
            'start_date': start_date,
            'end_date': end_date,
            'frequency_type': frequency,
            'daily_interval': int(daily_interval) if daily_interval else 1,
            'week_days': [int(item) for item in week_days] if week_days else [],
            'monthly_day': int(monthly_day) if monthly_day else 1,
            'error_message': None
        }



        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
        except Exception:
            context['error_message'] = 'Неверный формат даты. Используйте формат ГГГГ-ММ-ДД'
            return render(request, 'habbitadd.html', context=context)

        try:
            Habbit.objects.create(name=habbit_name, description=description, color_id=color_id,
                                  start_date=start_date, end_date=end_date, frequency=daily, user=request.user)
            return render(request, 'habbitadd.html', context=context)
        except ValidationError as e:
            context['error_message'] = e.messages[0]
            return render(request, 'habbitadd.html', context=context)
