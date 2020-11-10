from django.core.checks import messages
from django.shortcuts import redirect, render
import os
import json
from django.conf import settings
from .models import Currency
from django.contrib import messages
# Create your views here.


def currency(request):
    currency_data = []
    user_currency = None
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    if Currency.objects.filter(user=request.user).exists():
        user_currency = Currency.objects.get(user=request.user)

    if request.method == 'GET':
        context = {
            'currencies': currency_data,
            'user_currency': user_currency
        }
        return render(request, 'preferences/currency.html', context)
    else:
        currency = request.POST['currency']
        if Currency.objects.filter(user=request.user).exists():
            user_currency.currency = currency
            user_currency.save()
        else:
            Currency.objects.create(user=request.user, currency=currency)

        messages.success(request, 'Changes saved')
        context = {
            'currencies': currency_data,
            'user_currency': user_currency
        }
        return render(request, 'preferences/currency.html', context)
