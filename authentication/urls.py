from os import name
from .views import *
from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt, csrf_protect

urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', views.logoutView, name='logout'),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()),
         name="validate-username"),  # postman api test link: http://127.0.0.1:8000/auth/validate-username/
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()),
         name="validate-email"),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name="activate")
]
