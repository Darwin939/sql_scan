from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('make_analysis', views.make_analysis, name='make_analysis'),

]