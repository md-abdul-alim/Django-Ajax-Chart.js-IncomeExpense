
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.dashboard, name="incomes"),
    path('add-income/', views.add_income, name="add-income"),
    path('update-income/<int:id>', views.income_update, name="update-income"),
    path('delete-income/<int:id>', views.income_delete, name="delete-income"),
    path('search-income/', csrf_exempt(views.search_income), name="search-income"),

]
