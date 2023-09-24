from django.urls import path

from . import views

app_name = "primogems"
urlpatterns = [
    path("", views.primogems, name="primogems"),
    path('initialize/', views.initialize, name='initialize'),
]
