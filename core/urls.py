from django.urls import path
from . import views

urlpatterns = [
    path('', views.chart, name='chart'),
    path('bar/', views.yearly_avg_co2, name='bar'),
]