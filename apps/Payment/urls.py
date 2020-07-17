from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('charge/', views.charge, name='charge'),
    path('success/<str:args>/', views.successMsg, name='success'),
    path('createUser/', views.createCustomer, name='testing'),

    path('api/', views.apiOverview, name='apiOverview'),
    path('api/cus-list/', views.customerList, name='customer-list'),
    path('api/cus-detail/<str:pk>/', views.customerDetail, name='customer-detail'),
    path('api/cus-create/', views.customerCreate, name='customer-create'),
    path('api/cus-update/<str:pk>/', views.customerUpdate, name='customer-update'),
    path('api/cus-delete/<str:pk>/', views.customerDelete, name='customer-delete'),
]