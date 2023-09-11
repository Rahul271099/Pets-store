from django import forms
from django.contrib.auth.models import User
from .models import OrderPet,Payment,Orders

class orderForm(forms.ModelForm):
    status = (('new','new'),('pending','pending'),('deliverd','deliverd'),('cancelled','cancelled'))
    states = [('MH','Maharashtra'),('GOA','Goa'),('UP','Uttar Pradesh'),('RJ','Rajasthan'),('PNB','Punjab'),('GJ','Gujarat'),('BH','Bihar'),('HR','Haryana'),('UK','UttaraKhand'),('SK','Sikkim')] 

    first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    phone = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class':'form-control'}))
    country = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    state = forms.CharField(widget=forms.Select(choices=states,attrs={'class':'form-control'}))
    city = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Orders
        fields = ['first_name','last_name','phone','email','address','country','state','city']