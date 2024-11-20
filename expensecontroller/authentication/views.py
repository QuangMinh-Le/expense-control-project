import json
from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.cache import cache

from django.urls import reverse
from django.contrib import auth
# Create your views here.

class EmailValidationView(View):
   def post(self, request):
      data=json.loads(request.body)
      email = data['email']
      
      if not validate_email(email):
         return JsonResponse({'email_error': 'Email is invalid'}, status=400)
      
      if User.objects.filter(email=email).exists():
         return JsonResponse({'email_error': 'This email is use for another account, please use a different email'}, status=409)
      
      return JsonResponse({'email-valid': True})
   
class UsernameValidationView(View):
   def post(self, request):
      data=json.loads(request.body)
      username = data['username']
      
      if not str(username).isalnum():
         return JsonResponse({'username_error': 'username should only contains alphanumeric charactors'}, status=400)
      
      if User.objects.filter(username=username).exists():
         return JsonResponse({'username_error': 'username is taken, please choose another one'}, status=409)
      
      return JsonResponse({'username-valid': True})
   
class RegistrationView(View):
   def get(self, request):
      return render(request, 'authentication/register.html')
   def post(self, request):
      #Get user data
      username = request.POST["username"]
      email = request.POST["email"]
      password = request.POST["password"]
      
      context = {
         'fieldValues': request.POST
      }
      # Validate
      if not User.objects.filter(username = username).exists():
         if not User.objects.filter(email = email).exists():
            if len(password) < 6:
               messages.error(request, 'Password too short')
               return render(request, 'authentication/register.html', context)
            
            user = User.objects.create_user(username = username, email = email)
            user.set_password(password)
            user.is_active = True
            user.save()
            # email_subject="Activate your account"
            # email_body = "Test body test"
            # email = EmailMessage(
            #     email_subject,
            #     email_body,
            #     "noreply@semycolon.com",
            #     [email],
            # )
            
            # email.send(fail_silently=False)
            messages.success(request, 'Account successfully created')
            return render(request, 'authentication/register.html')
            
      return render(request, 'authentication/register.html')
   
class LoginView(View):
   def get(self, request):
      return render(request, 'authentication/login.html')
   
   def post(self, request):
      username = request.POST['username']
      password = request.POST['password']
      
      if username and password:
         user=auth.authenticate(username = username, password = password)
         if user: 
            auth.login(request, user)
            messages.success(request, "Welcome " + 
                             user.username+'! You are now logged in.')
            
            # Redirect to homepage
            return redirect('expenses')
         
         # NO user found
         messages.error(request, "Invalid credential. Please try again with another username or password.")
         return render(request, 'authentication/login.html')
      
      messages.error(request, "Please fill all fields")
      return render(request, 'authentication/login.html')
   
class LogoutView(View):
   def post (self, request):
      auth.logout(request)
      cache.clear()
      messages.success(request, "Successfully logged out.")
      return redirect('login')
   
class ResetPasswordView(View):
   
   def get(self, request):
      context = {}
      return render(request, 'authentication/reset-password.html', context)
   
   def post(self, request):
      context = {}
      email = request.POST['email']
      password=request.POST['password']
      confirmPassword=request.POST['confirmPassword']
      
      if password != confirmPassword: 
         messages.error(request, 'Password does not match')
         return render(request, 'authentication/reset-password.html', context)
      if len(password) < 6: 
         messages.error(request, 'Password too short')
         return render(request, 'authentication/reset-password.html', context)
      
      try:
         user = User.objects.get(email=email)
         user.set_password(password)
         user.save()
         
         messages.success(request, "New password saved successfully")
         return redirect('login')
      except Exception as identifier:
         messages.info(request, 'Somthing went wrong, please try again later.')
         return render(request, 'authentication/reset-password.html', context)
      