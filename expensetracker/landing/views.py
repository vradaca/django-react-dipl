from django.shortcuts import render

def landing_page(request):
    return render(request, r"frontend\build\index.html")

# Create your views here.
