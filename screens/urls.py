from django.urls import path

from . import views

app_name="screens"
urlpatterns = [
    path('', views.index, name='index'),
    path('otp/', views.otp, name='otp'),
    path('details/', views.UserDetails.as_view(), name='details'),
    path('validate_number/', views.validate_number, name='validate_number'),
    path('validate/', views.validate, name='validate'),
    path('validate_form/', views.validate_form, name='validate_form'),
    path('validate_login/', views.validate_login, name='validate_login'),
    path('filled/', views.filled, name='filled'),
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('chatting/', views.chatting, name='chatting'),
    path('message/', views.message, name='message'),
    path('news/', views.news, name='news'),
    path('logout/', views.logout, name='logout'),
]