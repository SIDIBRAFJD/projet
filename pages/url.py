from django.urls import path
from . import views
urlpatterns = [
    path('' , views.home,name='home'),
    path('phenology' , views.phenology,name='phenology'),
    path('about' , views.about,name='about'),
] 