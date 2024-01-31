from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("registrar/", views.registrar, name="registrar"),
    path("registrar/con_n/", views.con_n, name="con_n"),
  
    path("index/", views.index, name="index"),
    path('fulfillment/registrar/', views.registrar, name='registrar'),
     path("", views.fulfillment, name='fulfillment'),
    path('orders/', views.orders, name='orders'), 
    path('order_res/', views.order_res, name='order_res'),
    path('order_com/', views.order_com, name='order_com'),
    path("con_n/", views.con_n, name="con_n"),
    path("fulfillment/registrar/con_n/", views.con_n, name="con_n"),

    path('order_resq/order_res/', views.order_res, name='order_res'),
    path('order_resq/order_com/', views.order_com, name='order_com'),
     path("order_resq/con_n/", views.con_n, name="con_n"),
    path('order_resq/', views.order_resq, name='order_resq'),

    path('order_process/', views.order_process, name='order_process'),
    path('order_process/remove_p/', views.remove_p, name='remove_p'),
    path('order_process/robot_update/', views.robot_update, name='robot_update'),  
    path('fulfillment/order_process/', views.order_process, name='order_process'),
    path('load/', views.load, name='load'),
    path('load/getitem', views.getitem, name='getitem'),
     path('load/getitem1', views.getitem1, name='getitem1'),
    path('load/loadporo/', views.loadporo, name='loadporo'),
    
    path('order_process/order_fin/', views.order_fin, name='order_fin'),
    path('fulfillment/order_process/order_fin/', views.order_fin, name='order_process'),
    path("request_from_robot/", views.request_from_robot, name="request_from_robot"),  
    path("order_resq/request_from_robot/", views.request_from_robot, name="request_from_robot"),
    path('fulfillment/order_process/order_res/', views.order_res, name='order_res'),
    path('order_process/order_res/', views.order_res, name='order_res'),

     path('regf/', views.regf, name='regf'),
     path('fulfillment/regf/', views.regf, name='regf'),
    ]
    
