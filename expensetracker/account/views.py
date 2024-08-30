from django.shortcuts import render

def account_index(request):
    return(render(request, 'account/account.html'))
