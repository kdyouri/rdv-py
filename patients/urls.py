from django.urls import path, include
from django.urls.resolvers import URLPattern
from patients import views

urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('add', views.add),
    path('edit/<int:id>', views.edit),
    path('delete/<int:id>', views.delete)
]