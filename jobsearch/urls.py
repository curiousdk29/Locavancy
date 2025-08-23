from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_search, name='job_search'),
    path('load-nearby-places/', views.load_nearby_places, name='load_nearby_places'),
]
