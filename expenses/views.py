from django.core.checks import messages
from django.http import request
from expenses.models import Category
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Expense
from django.core.paginator import Paginator
# Create your views here.


@login_required(login_url='login')
def dashboard(request):
    #categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        # 'categories': categories,
        'expenses': expenses,
        'page_obj': page_obj
    }
    return render(request, 'expenses/dashboard.html', context)


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


def expense_delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense Deleted')
    return redirect('expenses')
