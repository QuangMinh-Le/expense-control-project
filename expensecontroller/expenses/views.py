from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from userpreferences.models import UserPreference
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

import datetime

# Create your views here.

def search_expenses(request):
   if request.method=='POST':
      search_str = json.loads(request.body).get('searchText')
      expenses=Expense.objects.filter(
         amount__istartswith=search_str, owner = request.user) | Expense.objects.filter(
         date__istartswith=search_str, owner = request.user) | Expense.objects.filter(
         description__icontains=search_str, owner = request.user) | Expense.objects.filter(
         category__icontains=search_str, owner = request.user)

      data = expenses.values()
      
      return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')

def index(request):
   categories = Category.objects.all()
   expenses=Expense.objects.filter(owner=request.user)
   paginator = Paginator(expenses, 4)
   page_number=request.GET.get('page')
   page_obj = Paginator.get_page(paginator, page_number)
   currency = UserPreference.objects.get(user=request.user).currency
   
   context={
      'expenses': expenses,
      'page_obj': page_obj,
      'currency': currency
   }
   return render(request, 'expenses/index.html', context)

def add_expense(request):
   categories = Category.objects.all()
   context = { 
            'categories': categories,
            'value': request.POST}
   
   if request.method == "GET":
      return render(request, 'expenses/add_expense.html', context)

   if request.method == 'POST':
      amount = request.POST['amount']
      description = request.POST['description']
      category = request.POST['category']
      date = request.POST['expense_date']
      
      if not amount: 
         messages.error(request, 'Amount is required')
         return render (request, 'expenses/add_expense.html', context)
   
      if not description: 
         messages.error(request, 'Description is required')
         return render (request, 'expenses/add_expense.html', context)
      
      if not date: 
         messages.error(request, 'Date is required')
         return render(request, 'expenses/add_expense.html', context)
      
      Expense.objects.create(owner = request.user, amount=amount, description=description, category=category,date=date)
      messages.success(request, 'Expense saved successfully!')
      
      return redirect('expenses')

def expense_edit(request, id):
   expense = Expense.objects.get(pk=id)
   categories = Category.objects.all()
   context = {
      'expense': expense,
      'value': expense,
      'categories': categories
   }
   if request.method == "GET":
      return render(request, 'expenses/edit_expense.html', context)
   if request.method == "POST":
      amount = request.POST['amount']
      description = request.POST['description']
      category = request.POST['category']
      date = request.POST['expense_date']
      
      if not amount: 
         messages.error(request, 'Amount is required')
         return render(request, 'expenses/edit_expense.html', context)
   
      
      if not description: 
         messages.error(request, 'Description is required')
         return render(request, 'expenses/edit_expense.html', context)
      
      if not date: 
         messages.error(request, 'Date is required')
         return render(request, 'expenses/edit_expense.html', context)
      
      expense.owner = request.user
      expense.amount=amount
      expense.description=description
      expense.category=category
      expense.date=date
      expense.save()
      messages.success(request, 'Expense saved successfully!')
      
      return redirect('expenses')

def delete_expense(request, id):
   expense = Expense.objects.get(pk=id)
   expense.delete()
   messages.success(request, 'Expense removed')
   return redirect('expenses')

def expense_category_summary(request): 
   today_date = datetime.date.today()
   six_months_ago = today_date - datetime.timedelta(days = 30 * 6)
   
   expenses = Expense.objects.filter(
      owner=request.user
      ,date__gte=six_months_ago
      ,date_lte=today_date)
   
   finalrep = {}
   
   def get_category(expense):
      return expense.category
   
   # Wrap in map() to remove duplicates
   category_list = list(set(map(get_category, expenses)))
   
   # Return the total amount of expense for each category
   def get_expense_category_amount(category):
      amount = 0
      filter_by_category = expenses.filter(category=category)
      for item in filter_by_category:
         amount+= item.amount
      return amount
   
   for x in expenses: 
      for y in category_list:
         finalrep[y]=get_expense_category_amount(y)
         
   return JsonResponse({'expenses_category_data': finalrep}, safe=False)


def stats_view (request):
   return render(request, 'expenses/stats.html')