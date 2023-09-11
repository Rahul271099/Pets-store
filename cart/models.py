from django.db import models
from first_app.models import pet
from django.contrib.auth.models import User

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=300,blank=True)
    Pet = models.ForeignKey(pet,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    totalprice = models.FloatField(default=0.00)
    timestamps = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart'
    
