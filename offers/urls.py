from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('product/<int:pk>/', views.productDetail, name='productDetail'),
    path('product/<int:pk>/api/', include('api.urls')),
]