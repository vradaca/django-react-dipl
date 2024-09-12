from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from userpreferences.models import UserPreference
from django.template.loader import render_to_string
from django.db.models import Sum
from weasyprint import HTML
import datetime
import json
import csv
import xlwt.Workbook
import tempfile

# Create your views here.

def search_expenses(request):
     if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(
            amount__istartswith = search_str, owner = request.user) | Expense.objects.filter(
            date__istartswith = search_str, owner = request.user) | Expense.objects.filter(
            description__istartswith = search_str, owner = request.user) | Expense.objects.filter(
            category__istartswith = search_str, owner = request.user)
        
        data = expenses.values()

        return JsonResponse(list(data), safe = False)

@login_required(login_url='/authentication/login')
@never_cache
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try: # Every new user has 'None' as their currency setting.
        currency = UserPreference.objects.get(user = request.user).currency # Thats why the query can't find it and we get it from the request
    except UserPreference.DoesNotExist:
         currency = request.GET.get('currencies')

    context = {
         'expenses': expenses, 
         'category': categories,
         'page_obj': page_obj, 
         'currency': currency, 
         'user': request.user
    }
    return render(request, 'expenses/index.html', context)

def add_expenses(request):

    categories = Category.objects.all()
    context = {
            'categories': categories, 
            'values': request.POST
            }

    if request.method == 'GET':
        
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':

        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST.get('category', None)

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        elif not description: 
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)
        elif not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/add_expense.html', context)
        elif not category:
            messages.error(request, 'Category is required')
            return render(request, 'expenses/add_expense.html', context)
        
        
    Expense.objects.create(owner= request.user, amount=amount, date=date, 
                           category=category, description=description)
    messages.success(request, 'Expense saved successfully')

    return redirect('expenses')

def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
         'expense':expense,
         'values': expense,
         'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit_expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not amount and amount.isdecimal():
            messages.error(request, 'Amount is required to be a number')
            return render(request, 'expenses/add_expense.html')
        elif not description: 
                messages.error(request, 'Description is required')
                return render(request, 'expenses/add_expense.html')
        
    expense.owner = request.user
    expense.amount = amount
    expense.date = date 
    expense.category = category
    expense.description = description

    expense.save()
    
    messages.success(request, 'Expense edited successfully')
    return redirect('expenses')

def expense_delete(request, id):
    expense = Expense.objects.get(pk = id)
    expense.delete()
    messages.success(request, 'Expense deleted')
    return redirect('expenses')

def expense_category_summary(request):
    todays = datetime.date.today()
    six_m_a = todays - datetime.timedelta(days = 30*6)
    expenses = Expense.objects.filter(owner = request.user, 
                                      date__gte = six_m_a, date__lte = todays) 
    finalrep = {}

    def get_category(expense):
          return expense.category

    category_list = list(set(map(get_category, expenses)))
     
    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category = category)

        for item in filtered_by_category:
             amount += item.amount

        return amount
    
    for exp in expenses:
          for cat in category_list:
               finalrep[cat] = get_expense_category_amount(cat)

    return JsonResponse({'expense_category_data': finalrep}, safe = False)

@login_required(login_url='/authentication/login')
@never_cache
def stats_view(request):
    return render(request, 'expenses/stats.html')
    
def export_csv(request):
     
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename = Expenses-' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount','Date of expense','Description','Category'])

    expenses = Expense.objects.filter(owner = request.user)

    for exp in expenses:
        writer.writerow([exp.amount, exp.date, exp.description, exp.category])

    return response

def export_xls(request):
    response = HttpResponse(content_type = 'application/ms_excel')
    response['Content-Disposition'] = 'attachment; filename = Expenses-' + str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount','Date','Description','Category']

    for col in range(len(columns)):
        ws.write(row_num, col, columns[col], font_style)

    font_style = xlwt.XFStyle()

    rows = Expense.objects.filter(owner = request.user).values_list('amount', 'date', 'description', 'category')

    for row in rows: 
        row_num +=1

        for col in range(len(row)):
             ws.write(row_num, col, str(row[col]), font_style)

    wb.save(response)

    return response

def export_pdf(request):
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'attachment; filename = Expenses-' + str(datetime.datetime.now()) + '.pdf'

    response['Content-Transfer-Encoding'] = 'binary'

    expenses = Expense.objects.filter(owner = request.user)

    sum = expenses.aggregate(Sum('amount'))

    html_string = render_to_string('expenses/pdf-output.html', {'expenses': expenses, 'total': sum['amount__sum']})
    html = html = HTML(string=html_string, base_url=request.build_absolute_uri())

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response