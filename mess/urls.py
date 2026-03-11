from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rate/<str:meal_type>/', views.rate_meal, name='rate_meal'),
    path('weekly/', views.weekly_trend, name='weekly_trend'),
]