import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
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