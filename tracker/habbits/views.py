from django.shortcuts import render

from .models import Color


# Create your views here.
def tracker(request):
    return render(request, 'tracker.html')

def habbit_add(request):
    if request.method == "GET":
        colors = Color.objects.all()
        return render(request,'habbitadd.html', context={'colors':colors})
    else:
        return render(request, 'habbitadd.html')