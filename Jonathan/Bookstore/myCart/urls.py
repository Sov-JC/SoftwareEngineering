from django.urls import path
from . import views

from django.views.generic import TemplateView
#book
#from django.conf.urls.defaults import *




#^notice django.urls import path, not django.urls import url

urlpatterns = [
    path('', views.index, name='index'),             
    path('myCart/', views.index, name="myCart"),    
    path('example/', views.example, name="example"),
    

    #testing ---------------------------------------------------------
    #path('session/', views.consoleSessionDisplay, name="session"),    
    path('createCookieTest/', views.createCookieTest, name="createCookieTest"),
    path('cookieInfo/', views.cookieInfo, name='cookieInfo'),
    path('makeCartCookie/', views.makeCartCookie, name='makeCartCookie'),
    #path('session/', views.indexSession, name="indexsession"),
    #path('login_page/', views.login_page, name="loginpage"),    
    path('homepage/', views.homepage, name="homepage")
    #path('errorpage/', views.errorpage, name="errorpage"),
    
]