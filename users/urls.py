from django.urls import path
from users import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('login', LoginView.as_view(template_name='users/login.html', next_page='/')),
    path('logout', LogoutView.as_view(next_page='/users/login')),
    path('add', views.add),
    path('edit/<int:id>', views.edit),
    path('delete/<int:id>', views.delete)
]