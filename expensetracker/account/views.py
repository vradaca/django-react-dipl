from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


@login_required(login_url='/authentication/login')
@never_cache
def account_index(request):
    return(render(request, 'account/account.html'))
