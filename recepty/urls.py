from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'recepty'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='recepty:index'), name='logout'),
    path('recept/novy/', views.ReceptCreateView.as_view(), name='recept-create'),
    path('recept/<int:pk>/upravit/', views.ReceptUpdateView.as_view(), name='recept-update'),
    path('recept/<int:pk>/smazat/', views.ReceptDeleteView.as_view(), name='recept-delete'),
]
