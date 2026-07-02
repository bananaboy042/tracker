from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Color


@login_required
def tracker(request):
    return render(request, 'tracker.html')

@login_required
def habbit_add(request):
    if request.method == "GET":
        colors = Color.objects.all()
        return render(request,'habbitadd.html', context={'colors':colors})
    else:
        return render(request, 'habbitadd.html')