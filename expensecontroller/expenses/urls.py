from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="expenses"),
    path('add-expense', views.add_expense, name="add-expense"),
    path('edit-expense/<int:id>', views.expense_edit, name="expense_edit"),
    path('delete-expense/<int:id>', views.delete_expense, name="delete-expense")
]
