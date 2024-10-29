from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages

# Create your views here.

@login_required(login_url='/authentication/login')

def index(request):
   categories = Category.objects.all()
   expenses=Expense.objects.filter(owner=request.user)
   
   context={
      'expenses': expenses,
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
         return render(request, 'expenses/edit_expense.html', context)
      
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