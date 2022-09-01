from django.urls import path
from . import views

app_name = 'recommender'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.MealCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', views.MealDetail.as_view(), name='detail'),
    path('get_detail/<int:pk>/', views.meal_detail_axios, name='detail_axios'),
]
