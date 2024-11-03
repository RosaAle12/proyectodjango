from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='auth-login-basic') 
def home_views(request):
    template_name = "index.html" 
    
    return render(request,template_name)