from django.db import models
from first_app.models import pet
from django.contrib.auth.models import User

class Payment(models.Model):
    payment_id = models.CharField(max_length=200)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount_paid = models.CharField(max_length=150)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
    
class Orders(models.Model):
    status = (('new','new'),('pending','pending'),('deliverd','deliverd'),('cancelled','cancelled'))

    states = [('MH','Maharashtra'),('GOA','Goa'),('UP','Uttar Pradesh'),('RJ','Rajasthan'),('PNB','Punjab'),('GJ','Gujarat'),('BH','Bihar'),('HR','Haryana'),('UK','UttaraKhand'),('SK','Sikkim')]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_bumber = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100,choices=states,default='MH')
    country = models.CharField(max_length=100)
    total = models.FloatField()
    status = models.CharField(max_length=100,choices=status,default='new')
    ip = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)

    def __str__(self):
        return self.user.first_name
    
class OrderPet(models.Model):
    order_id = models.ForeignKey(Orders,on_delete=models.CASCADE,default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    Pet = models.ForeignKey(pet,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    pet_price =models.FloatField()
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)

    def __str__(self):
        return self.Pet.name
