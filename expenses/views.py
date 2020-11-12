from django.core.checks import messages
from django.http import request
from django.http import response
from expenses.models import Category
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Expense
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
from userpreferences.models import Currency
import datetime
import csv
import xlwt

'''
from django.template.loader import render_to_string
from weasyprint import html
import tempfile
from django.db.models import Sum
'''
# Create your views here.


@login_required(login_url='login')
def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            category__icontains=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
                amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
                    date__istartswith=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='login')
def dashboard(request):
    #categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = Currency.objects.get(user=request.user).currency
    except Currency.DoesNotExist:
        currency = 'Set Currency'

    context = {
        # 'categories': categories,
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'expenses/dashboard.html', context)


@login_required(login_url='login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }

    if request.method == 'POST':
        category = request.POST['category']
        description = request.POST['description']
        amount = request.POST['amount']
        date = request.POST['date']
        # import pdb
        # pdb.set_trace()
        if not amount:
            messages.error(request, 'amount is required')
            return render(request, 'expenses/add_expense.html', context)

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(
            owner=request.user,
            category=category,
            description=description,
            amount=amount,
            date=date
        )
        messages.success(request, 'Expense saved successfully')
        return redirect('expenses')

    return render(request, 'expenses/add_expense.html', context)


@login_required(login_url='login')
def expense_update(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/update_expense.html', context)

    if request.method == 'POST':
        category = request.POST['category']
        description = request.POST['description']
        amount = request.POST['amount']
        date = request.POST['date']
        # import pdb
        # pdb.set_trace()
        if not amount:
            messages.error(request, 'amount is required')
            return render(request, 'expenses/update_expense.html', context)

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/update_expense.html', context)
        if not date:
            messages.error(request, 'date is required')
            return render(request, 'expenses/update_expense.html', context)

        expense.owner = request.user
        expense.category = category
        expense.description = description
        expense.amount = amount
        expense.date = date
        expense.save()

        messages.success(request, 'Expense updated successfully')
        return redirect('expenses')


@login_required(login_url='login')
def expense_delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense Deleted')
    return redirect('expenses')


def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)

    final_representation = {}

    # take a expense and return catogory for that expense
    def get_category(expense):
        return expense.category
    # Return category for each expense
    # this will return a category list
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount

        return amount

    for x in expenses:
        for y in category_list:
            final_representation[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': final_representation}, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')


def export_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = Expenses' + \
        str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    # this will be header
    writer.writerow(['Category', 'Description', 'Amount', 'Date'])

    expenses = Expense.objects.filter(owner=request.user)

    # this will be data
    for expense in expenses:
        writer.writerow([expense.category, expense.description,
                         expense.amount, expense.date])
    return response

# https://xlwt.readthedocs.io/en/latest/installation.html
# pip install xlwt


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename = Expenses' + \
        str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Category', 'Description', 'Amount', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = Expense.objects.filter(owner=request.user).values_list(
        'category', 'description', 'amount', 'date')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)
    return response

# pip install WeasyPrint
# https://pypi.org/project/WeasyPrint/#description


# Not completed
# def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename = Expenses' + \
        str(datetime.datetime.now())+'.pdf'

    response['Content-Transfer-Encoding'] = 'binary'

    html_string = render_to_string(
        'expenses/pdf-output.html', {'expenses': [], 'total': 0})

    html = html(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(request)
        output.flush()

        output = open(output.name, 'rb')
        response.write(output.read())

    return response


def export_pdf(request):
    pass
