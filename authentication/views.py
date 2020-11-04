from email_validator import validate_email, EmailNotValidError
from validate_email import validate_email
from django.http import request
from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages


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


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use, choose another one'}, status=409)

        return JsonResponse({'email_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):

        # messages.success(request, 'Success Registration')submit-btn
        # messages.warning(request, 'Success Registration warning')
        # messages.info(request, 'Success Registration info')
        # messages.error(request, 'Success Registration error')

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password) < 6:
                    messages.error(
                        request, 'Password too short. It should be at least 6.')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                #user = User.objects.create(username=username, email=email)
                user.set_password(password)
                user.save()
                messages.success(request, 'Account successfully created.')
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')
