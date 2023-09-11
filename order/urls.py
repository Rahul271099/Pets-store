from django.urls import path
from .import views

app_name = "order"
urlpatterns = [
    path('billing/',views.place_order,name="place_order"),
    path('order_history/',views.show_orders,name='show_orders'),
    path('payment/',views.payments,name="payments")
]
    