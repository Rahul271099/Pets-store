from typing import Optional
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib import messages
from first_app.views import pets_list   
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
# Create your views here.

def register(request):
    if request.method == "GET":
        form = RegistrationForm()
        return render(request,'base/register.html',{'form_data':form})
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            messages.success(request,'Account Created Successfully for'+ user_name)
            return redirect(pets_list)
        else:
            messages.error(request,"Please Check your form there is some issues in form")
            return render(request,'base/register.html',{'form_data':form})
        
    return render(request,'base/register.html',{'form_data':form})

class myLoginView(LoginView):
    def form_valid(self,form):
        messages.success(self.request,'Logged in succesfully')
        return super().form_valid(form)
    def form_invalid(self,form):
        messages.error(self.request,'Invalid Credentials!!!!')
        return super().form_invalid(form)
    
class myLogout(LogoutView):
    def get_next_page(self):
        messages.success(self.request,"Logout Successfully")
        return reverse_lazy('home')

def account_info(request):
    acc_data  = User.objects.get(username = request.user)
    context = {
        'acc_data':acc_data
    }
    if acc_data:
        return render(request,"account/account_info.html",context)
    else:
        messages.error("Please Login to access this data!!!!!!")
        return redirect("login_page")
    

