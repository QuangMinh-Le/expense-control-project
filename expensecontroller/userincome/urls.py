from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name="income"),
    path('add-income', views.add_expense, name="add-income"),
    path('edit-income/<int:id>', views.expense_edit, name="expense_edit"),
    path('delete-income/<int:id>', views.delete_expense, name="delete-income"),
    path('search-income', csrf_exempt(views.search_expenses), name="search-income")
]
