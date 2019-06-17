from django.shortcuts import render
from app import settings
# Create your views here.
from django.http import HttpResponse
from django.template import loader
import http.client
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Users,Message
from random import randint
from django.http import JsonResponse
from bootstrap_datepicker_plus import DateTimePickerInput
from django.db.models import Q
from .filter import UserFilter
from django.core import serializers
import json
from bs4 import BeautifulSoup
import requests
def index(request):
   return render(request, 'index.html')

def otp(request):
   if type(request.POST.get("number")) == str:
      if len(request.POST.get("number")) == 10 and request.POST.get("number").isnumeric():
         otp = ''
         for i in range(6):
            otp += str(randint(0,9))
         conn = http.client.HTTPConnection("api.msg91.com")

         conn.request("GET", "http://api.msg91.com/api/sendhttp.php?route=4&sender=INTREF&mobiles="+request.POST.get("number")+"&authkey=?&message=Your verification code is "+otp+"&country=91")
         res = conn.getresponse()
         data = res.read()
         request.session['otp'] = otp

        
      
         return render(request, 'otp.html')
   errors = []
   errors.append('Enter a valid Number')
   return render(request, 'index.html', {'errors': errors})

def validate_number(request):
   number = request.GET.get('number', None)
   if Users.objects.filter(number__iexact=number).exists() != 0:
      data = {
        'is_taken': Users.objects.filter(number__iexact=number).exists()
    }
      return JsonResponse(data)
   else:
      data = {
        'is_taken': False
      }
      request.session['number'] = number
      return JsonResponse(data)


def validate(request):
   number = request.GET.get('otp')
   if number == request.session['otp']:
      data = {
        'is_taken': True
      }
      return JsonResponse(data)
   else:
      data = {
        'is_taken': False
      }
      return JsonResponse(data)

   



class UserDetails(CreateView):
    model = Users
    fields = ['name','country','gender','BirthDate','password','username']
    def get_form(self):
        form = super().get_form()
        form.fields['BirthDate'].widget = DateTimePickerInput()
        return form

def validate_form(request):
   username = request.GET.get('username', None)
   if Users.objects.filter(username__iexact=username).exists() != 0:
      data = {
        'is_taken': Users.objects.filter(username__iexact=username).exists()
    }
      return JsonResponse(data)
   else:
      data = {
        'is_taken': False
      }
      return JsonResponse(data)


def validate_login(request):
   username = request.GET.get('username', None)
   password = request.GET.get('password', None)
   if Users.objects.filter(Q(username=username) & Q(password=password)).exists() != 0:
      data = {
        'is_taken': Users.objects.filter(Q(username=username) & Q(password=password)).exists()} 
      request.session['username'] = username
      return JsonResponse(data)
   else:
      data = {
        'is_taken': False
      }
      return JsonResponse(data)
   
def logout(request):
   keys = []
   for key in request.session.keys():
      if key =='username':
         keys.append(key)
   for key in keys:
      del request.session[key]
   return render(request, 'index.html')

def filled(request):
   user = Users()
   user.number = request.session['number']
   user.gender = request.POST.get('gender')
   user.BirthDate = request.POST.get('BirthDate')
   user.name = request.POST.get('name')
   user.country = request.POST.get('country')
   user.password = request.POST.get('password')
   user.username = request.POST.get('username')
   user.save()
   context ={"message": "You have successfully logged in."}
   keys = []
   for key in request.session.keys():
      if key =='otp' or key =='number':
         keys.append(key)
   for key in keys:
      del request.session[key]
   return render(request, 'index.html',context)

def home(request):
   print(request.session['username'])
   if request.session['username'] != None:
      username = request.session['username']
      user = Users.objects.filter(username=username)
      user_list = Users.objects.filter(~Q(username=username))
      # suffix = [i.file_suffix for i in user]
      context = {
         'user':user,
         'users_filter':user_list
      }
      print()
      return render(request, 'homescreen.html',context)
   else:
      return render(request, 'index.html')

def search(request):
   name = request.GET.get('username', None)
   username = request.session['username']
   user_list = Users.objects.filter(~Q(username=username) & Q(Q(username__contains=name)| Q(number__contains=name)))
   response_data = {}
   try:
      response_data['result'] = 'Success'
      response_data['message'] = serializers.serialize('json', user_list)
   except:
      response_data['result'] = 'Ouch!'
      response_data['message'] = 'Script has not ran correctly'
   print(response_data)
   return JsonResponse(response_data)


def chatting(request):
   user = request.session['username']
   friend = request.GET.get('id', None)
   print(user,friend)
   data = Users.objects.filter(Q(username=friend))
   udata = Users.objects.filter(Q(username=user))
   user_list = Message.objects.filter(Q(Q(sender=user)| Q(reciever=user)) & Q(Q(sender=friend)| Q(reciever=friend)))
   response_data = {}
   if user_list.exists():
      response_data['message'] = serializers.serialize('json', user_list)
   else:
      response_data['message'] = 'empty'
      print("None")
   response_data['friend'] = serializers.serialize('json', data)
   response_data['user'] = serializers.serialize('json', udata)
   return JsonResponse(response_data)


def message(request):
   if request.session['username'] != '' or request.session['username'] != None:
      sender = request.session['username']
      friend = request.GET.get('friend', None)
      message = request.GET.get('message', None)
      print(sender,friend,message)
      user = Message()
      user.sender = sender
      user.reciever = friend
      user.message = message
      user.save()
      response_data ={}
      user_list = Message.objects.filter(Q(Q(sender=user)| Q(reciever=user)) & Q(Q(sender=friend)| Q(reciever=friend)))
      if user_list.exists():
         print(user_list)
         response_data['message'] = serializers.serialize('json', user_list)
      else:
         response_data['message'] = 'empty'
         print("None")
      print(response_data)
      return JsonResponse(response_data)
   else:
      return render(request,'index.html')



def news(request):
   if request.session['username'] != None:
      print(request.session['username'])
      username = request.session['username']
      url = 'https://www.indiatoday.in/rss'
      page = requests.get(url)
      soup = BeautifulSoup(page.text, 'html.parser')
      domains = soup.find_all("ul", class_="links")
      length = []
      data = {}
      i=0
      for a in domains[0].findAll('a'):
         data[i] = {"name":a.contents[0],"link":a['href']}
         length.append(i)
         i+=1
      user = Users.objects.filter(username=username)

      context = {
         'newsname':data,
         "length":length,
         "user":user
      }
      return render(request, 'homescreen.html', context)
   else:
      print("No")
      return render(request, 'index.html')
