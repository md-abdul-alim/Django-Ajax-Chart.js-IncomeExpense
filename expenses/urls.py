
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.dashboard, name="expenses"),
    path('add-expense/', views.add_expense, name="add-expense"),
    path('update-expense/<int:id>', views.expense_update, name="update-expense"),
    path('delete-expense/<int:id>', views.expense_delete, name="delete-expense"),
    path('search-expenses/', csrf_exempt(views.search_expenses), name="search-expenses"),

]
