from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference

# Create your views here.

def search_income(request):
     if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        incomes = Income.objects.filter(
            amount__istartswith = search_str, owner = request.user) | Income.objects.filter(
            date__istartswith = search_str, owner = request.user) | Income.objects.filter(
            description__istartswith = search_str, owner = request.user) | Income.objects.filter(
            source__istartswith = search_str, owner = request.user)
        
        data = incomes.values()

        return JsonResponse(list(data), safe = False)

@login_required(login_url='/authentication/login')
def index(request):
    sources = Source.objects.all()
    incomes = Income.objects.filter(owner=request.user)
    paginator = Paginator(incomes, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try: # Every new user has 'None' as their currency setting.
        currency = UserPreference.objects.get(user = request.user).currency # Thats why the query can't find it and we get it from the request
    except UserPreference.DoesNotExist:
         currency = request.GET.get('currencies')

    context = {
         'incomes': incomes, 
         'source': sources,
         'page_obj':page_obj, 
         'currency':currency
    }
    return render(request, 'income/index.html', context)

def add_income(request):

    sources = Source.objects.all()
    context = {
            'sources': sources, 
            'values': request.POST
            }

    if request.method == 'GET':
        
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html')
        elif not description: 
                messages.error(request, 'Description is required')
                return render(request, 'income/add_income.html')
        
    Income.objects.create(owner = request.user, amount = amount, date = date, 
                           source = source, description = description)
    messages.success(request, 'Income saved successfully')

    return redirect('income')

def income_edit(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
         'income': income,
         'values': income,
         'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        sources = request.POST['sources']

        if not amount and amount.isdecimal():
            messages.error(request, 'Amount is required to be a number')
            return render(request, 'income/add_income.html')
        elif not description: 
                messages.error(request, 'Description is required')
                return render(request, 'income/add_income.html')
        
    income.owner = request.user
    income.amount = amount
    income.date = date 
    income.source = sources
    income.description = description

    income.save()
    
    messages.success(request, 'income edited successfully')
    return redirect('income')

def income_delete(request, id):
    income = Income.objects.get(pk = id)
    income.delete()
    messages.success(request, 'income deleted')
    return redirect('income')