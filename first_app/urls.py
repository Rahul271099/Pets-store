from django.urls import path
from .views import pets_list, pets_details,dog_list,cat_list,search_results2

urlpatterns = [
    path('pets_list/',pets_list,name='pets_list'),
    path('pets_details/<int:pk>',pets_details,name="pet_details"),
    path('pets_list/dog_list',dog_list,name='dog-list'),
    path('pets_list/cat_list',cat_list,name='cat-list'), 
    path('pets_list/search/',search_results2,name='search'), 
    
]