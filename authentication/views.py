from email_validator import validate_email, EmailNotValidError
from validate_email import validate_email
from django.http import request
from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User


# Create your views here.


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use, choose another one'}, status=409)

        return JsonResponse({'username_valid': True})


# this is for froguction: pip install email-validator #https://pypi.org/project/email-validator/
#from email_validator import validate_email, EmailNotValidError
# this is for api test: pip install validate_email #https://pypi.org/project/validate_email/#description
from validate_email import validate_email


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use, choose another one'}, status=409)

        return JsonResponse({'email_valid': True})

        # try:
        #     # Validate.
        #     valid = validate_email(email)

        #     # Update with the normalized form.
        #     email = valid.email
        # except EmailNotValidError as e:
        #     # email is not valid, exception message is human-readable
        #     print(str(e))
        #raise EmailSyntaxError("The email address is not valid. It must have exactly one @-sign.")
        # email_validator.EmailSyntaxError: The email address is not valid. It must have exactly one @-sign.


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
