from django.core.checks import messages
from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Source, Income
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import Currency
# Create your views here.


@login_required(login_url='login')
def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        incomes = Income.objects.filter(
            source__icontains=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter(
                amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
                    date__istartswith=search_str, owner=request.user)
        data = incomes.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='login')
def dashboard(request):
    incomes = Income.objects.filter(owner=request.user)
    paginator = Paginator(incomes, 3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = Currency.objects.get(user=request.user).currency
    except Currency.DoesNotExist:
        currency = 'Set Currency'

    context = {
        # 'categories': categories,
        'incomes': incomes,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'incomes/dashboard.html', context)


@login_required(login_url='login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }

    if request.method == 'POST':
        source = request.POST['source']
        description = request.POST['description']
        amount = request.POST['amount']
        date = request.POST['date']
        # import pdb
        # pdb.set_trace()
        if not amount:
            messages.error(request, 'amount is required')
            return render(request, 'incomes/add_income.html', context)

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'incomes/add_income.html', context)

        Income.objects.create(
            owner=request.user,
            source=source,
            description=description,
            amount=amount,
            date=date
        )
        messages.success(request, 'Income rocord saved successfully')
        return redirect('incomes')

    return render(request, 'incomes/add_income.html', context)


@login_required(login_url='login')
def income_update(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'incomes/update_income.html', context)

    if request.method == 'POST':
        source = request.POST['source']
        description = request.POST['description']
        amount = request.POST['amount']
        date = request.POST['date']
        # import pdb
        # pdb.set_trace()
        if not amount:
            messages.error(request, 'amount is required')
            return render(request, 'incomes/update_income.html', context)

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'incomes/update_income.html', context)
        if not date:
            messages.error(request, 'date is required')
            return render(request, 'incomes/update_income.html', context)

        income.owner = request.user
        income.source = source
        income.description = description
        income.amount = amount
        income.date = date
        income.save()

        messages.success(request, 'Income updated successfully')
        return redirect('incomes')


@login_required(login_url='login')
def income_delete(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income Deleted')
    return redirect('incomes')
