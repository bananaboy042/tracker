from django.shortcuts import render

# Create your views here.
def tracker(request):
    return render(request, 'tracker.html')