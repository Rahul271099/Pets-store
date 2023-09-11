from django.urls import path
from .import views

urlpatterns = [
    path('add_to_cart/<int:id>',views.add_to_cart,name="add_to_cart"),
    path('cart_data/',views.show_all_cart_view,name="all_data_cart"),
    path('updatecart/<int:id>/',views.update_cart,name="updatecart"),
    path('cart_data/delete/<int:id>',views.delete_view,name="delete_data_cart"),
]
