from django.urls import path
from . import views

app_name = 'trade'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:hostport>/', views.detail, name='detail')
]