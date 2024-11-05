from django.shortcuts import redirect, render
from .models import Source, UserIncome
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/authentication/login')

def index(request):
   sources = Source.objects.all()
   income=UserIncome.objects.filter(owner=request.user)
   paginator = Paginator(income, 4)
   page_number=request.GET.get('page')
   page_obj = Paginator.get_page(paginator, page_number)
   currency = UserPreference.objects.get(user=request.user).currency
   
   context={
      'income': income,
      'page_obj': page_obj,
      'currency': currency
   }
   return render(request, 'income/index.html', context)

def add_income(request):
   sources = Source.objects.all()
   context = { 
            'sources': sources,
            'value': request.POST}
   
   if request.method == "GET":
      return render(request, 'income/add_income.html', context)

   if request.method == 'POST':
      amount = request.POST['amount']
      description = request.POST['description']
      source = request.POST['source']
      date = request.POST['income_date']
      
      if not amount: 
         messages.error(request, 'Amount is required')
         return render (request, 'income/add_income.html', context)
   
      if not description: 
         messages.error(request, 'Description is required')
         return render (request, 'income/add_income.html', context)
      
      if not date: 
         messages.error(request, 'Date is required')
         return render(request, 'income/add_income.html', context)
      
      UserIncome.objects.create(owner = request.user, amount=amount, description=description,source = source,date=date)
      messages.success(request, 'Income saved successfully!')
      
      return redirect('income')