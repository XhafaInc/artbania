from django.contrib import admin
from django.urls import path
from accounts.views import LoginView
from accounts import views
app_name='accounts'
urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',views.logout_view,name='logout'),
]
