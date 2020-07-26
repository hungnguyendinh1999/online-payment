from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('charge/', views.charge, name='charge'),
    path('success/<str:args>/', views.successMsg, name='success'),

    # API calls
    path('api/', views.apiOverview, name='apiOverview'),

    path('api/customers/', views.CustomerList.as_view()),
    path('api/customers/<str:pk>/', views.CustomerDetail.as_view()),
    
    path('api/cards/', views.CardList.as_view()),
    path('api/cards/<str:pk>/', views.cardDetail, name='card-detail'), #retrieve a card
    path('api/cards/<str:pk>/', views.cardUpdate, name='card-update'),
    path('api/cards/<str:pk>/', views.cardDelete, name='card-delete'),
]