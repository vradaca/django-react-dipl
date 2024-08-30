from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth 
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import token_generator
import threading
import json
from validate_email import validate_email

class EmailThread(threading.Thread):

    def __init__(self, emailMsg):
        self.emailMsg = emailMsg
        threading.Thread.__init__(self)

    def run(self):
        self.emailMsg.send(fail_silently = False)

class EmailValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status = 400)
        if User.objects.filter(email = email).exists():
            return JsonResponse({'email_error':'Sorry, email in use, please choose another one'}, status = 400)
        
        return JsonResponse({'email_valid': True})
    
class UsernameValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status = 400)
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error':'Sorry, username in use, please choose another one'}, status = 400)
        
        return JsonResponse({'username_valid': True})

class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')
    
    def post(self,request):

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {

            'field_values': request.POST

        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(username=username).exists():

                if len(password) < 7:
                    messages.error(request, 'Password too short')
                    return render(request,'authentication/register.html', context)
                
                user = User.objects.create_user(username = username, email = email)
                user.set_password(password)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs = {
                               'uidb64':uidb64,
                                'token':token_generator.make_token(user)
                                })
                active_url = 'http://' + domain + link


                email_body = 'Hello ' + user.username + '\nThank you for signing up for BudgetTracker!\n' + 'Please verify your email address before you can login! \n\n' + active_url
                emailMsg = EmailMessage(
                    'Activate Your Account - BudgetTracker',
                    email_body,
                    'noreply@budgettracker.com',
                    [email]
                )
                EmailThread(emailMsg).start()

                messages.success(request, 'Account succesfully created')
                return render(request,'authentication/login.html')

        return render(request,'authentication/register.html')
    
class VerificationView(View):
    def get(self, request, uidb64, token):

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = id)

            if not token_generator.check_token(user, token):
                return redirect('login' + '?message=' + 'User already activated')


            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')
    
class LoginView(View):
    def get(self,request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username'] 
        password = request.POST['password'] 

        if username and password:
            user = auth.authenticate(username = username, password = password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username + ' you are now logged in')
                    return redirect('expenses')
                    
                messages.error(request, 'Account is not active, please check your email')
                return render(request, 'authentication/login.html')
            
            messages.error(request, 'Invalid credentials, try again')
            return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'Succesfuly logged out!')
        return redirect('login')
    
class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')
    
    def post(self, request):

        email = request.POST['email']

        context ={
            'values': request.POST
        }

        if not validate_email(email):
            messages.error(request, 'Please supply a valid email')
            return render(request, 'authentication/reset-password.html', context)
        
        user = User.objects.filter(email = email)

        domain = get_current_site(request).domain
        if user.exists():
            email_content = {
            'user': user[0], 
            'domain': domain, 
            'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
            'token': PasswordResetTokenGenerator().make_token(user[0])
                            }

        link = reverse('set-new-password', kwargs = {
                               'uidb64': email_content['uid'],
                                'token':email_content['token']
                                })
        
        reset_url = 'https://' + domain + link

        emailMsg = EmailMessage(
            'Password reset Instructions - BudgetTracker',
            'Hi!  ' + user[0].username + '\nPlease click the link below to reset your password! \n\n' + reset_url,
            'noreply@budgettracker.com',
            [email]
            )
        EmailThread(emailMsg).start()

        messages.success(request, 'We have sent you an e-mail to reset your password')
        return render(request,'authentication/reset-password.html')
    
class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        context={
            'uidb64': uidb64,
            'token': token
        }

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Password link is invalid request a new one')
                return render(request, 'authentication/reset-password.html')
        
        except Exception as ex:

            pass

        return render(request, 'authentication/set-new-password.html', context)
    

    def post(self, request, uidb64, token):
        context={
            'uidb64': uidb64,
            'token': token
        }

        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'authentication/set-new-password.html', context)
        
        if len(password) < 8:
            messages.error(request, 'Password is less than 8 characters. Please try again!')
            return render(request, 'authentication/set-new-password.html', context)
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = user_id)
            user.set_password(password)
            user.save()

            messages.success(request, 'Password reset succesfully!')
            return redirect('login')
        
        except Exception as ex:
            messages.error(request, 'Something went wrong, please try again later')
            return render(request, 'authentication/set-new-password.html', context)        
        
class DeleteUser(View):
    def post(self, request, id):
        auth.logout(request)
        User.objects.get(pk = id).delete()
        messages.success(request, "User succesfully deleted")
        return redirect('login')