from django.urls import path
from home import views
from django.http import HttpResponse

urlpatterns = [
     path('', views.index, name='home'),
     path('about/', views.about, name='about'),
     path('contact/', views.contact, name='contact'),
     path('prediction/', views.prediction, name='prediction'),
     path('login/', views.login, name='login'),
     path('registration/', views.registration, name='registration'),
     path('test/',lambda request: HttpResponse('Test page'), name='test'),

]