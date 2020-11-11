from django.core.checks import messages
from django.http import request
from expenses.models import Category
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Expense
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import Currency
import datetime
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
