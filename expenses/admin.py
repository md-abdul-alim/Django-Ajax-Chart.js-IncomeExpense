from django.contrib import admin
from .models import Expense, Category
# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):

    list_display = ('owner','category','description','amount','date',)
    search_fields = ('category','description','amount','date',)
admin.site.register(Expense,ExpenseAdmin)
admin.site.register(Category)
