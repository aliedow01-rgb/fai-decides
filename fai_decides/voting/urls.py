from django.urls import path
from. import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stk/', views.stk_push, name='stk'),
    path('callback/', views.callback, name='callback'),
]