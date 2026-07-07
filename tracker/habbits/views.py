from django.contrib.auth.decorators import login_required
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
        if frequency == 'daily':
            daily_interval = request.POST.get('daily_interval', '')
            daily = {'type': frequency, 'interval': int(daily_interval)}
            # print(daily_interval)
        elif frequency == 'weekly':
            week_days = request.POST.getlist('week_days', '')
            daily = {'type': frequency, 'days': [int(item) for item in week_days]}

            # print(week_days)
        else:
            monthly_day = request.POST.get('monthly_day', '')
            daily = {'type': frequency, 'day': int(monthly_day)}
#             print(monthly_day)
        print(habbit_name, description, color_id, start_date, end_date, frequency,request.user )
        Habbit.objects.create(name=habbit_name, description=description, color_id=color_id,
                              start_date=start_date, end_date=end_date, frequency=daily, user=request.user)
        return render(request, 'habbitadd.html',context={'colors':colors})