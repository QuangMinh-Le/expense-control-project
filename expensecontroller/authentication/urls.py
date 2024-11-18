from .views import LogoutView, RegistrationView, UsernameValidationView, EmailValidationView, LoginView, ResetPasswordView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt, csrf_protect


urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name="validate-email"),
    path('reset-password', csrf_exempt(ResetPasswordView.as_view()), name="reset-password"),
]
