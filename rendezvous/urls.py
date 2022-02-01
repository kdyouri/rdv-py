from django.urls import path
from rendezvous import views

urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('feed', views.feed),
    path('add', views.add),
    path('edit/<int:id>', views.edit),
    path('delete/<int:id>', views.delete)
]