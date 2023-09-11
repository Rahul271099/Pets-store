from django.contrib import admin
from .models import pet
from cart.models import Cart
from order.models import Orders,Payment,OrderPet
from django.utils.html import format_html



class CustomAdmin(admin.ModelAdmin):
    list_display = ['name','Species','breed','description','image_tag']
    list_filter = ['gender','breed']
    search_fields = ["Species","name"]

    def image_tag(self, obj):
        return format_html('<img src="{}" style="width:100px; height:100px; border-radius:10%; object-fit:cover"/>',obj.image.url)

class PaymentCustom(admin.ModelAdmin):
    list_display = ['payment_id','status']
class OrderCustom(admin.ModelAdmin):
    list_display=['user','status']
class OrderPetCustom(admin.ModelAdmin):
    list_display=['']

# Register your models here.
admin.site.register(pet,CustomAdmin)
admin.site.register(Orders,OrderCustom)
admin.site.register(Payment,PaymentCustom)
admin.site.site_header = 'Admin Panel'
admin.site.site_title = 'Admin'
admin.site.index_title = 'Pet Store Administrator'



