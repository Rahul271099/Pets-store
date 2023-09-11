from django.urls import path
from .views import register,myLoginView,myLogout,account_info

urlpatterns = [
    path('register/',register,name='register_page'),
    path('login/',myLoginView.as_view(template_name = 'base/login.html'),name='login_page'),
    path('logout/',myLogout.as_view(),name='logout'),
    path('account_info/',account_info,name='account_info'),
]