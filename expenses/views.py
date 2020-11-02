from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, 'expenses/dashboard.html')


def index(request):
    return render(request, 'index.html')


def add_expense(request):
    return render(request, 'expenses/add_expense.html')
