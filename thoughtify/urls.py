from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('feed/', views.feed, name='feed'),
    path('thought/create/', views.create_thought, name='create_thought'),
    path('thought/<int:thought_id>/update/', views.update_thought, name='update_thought'),
    path('thought/<int:thought_id>/delete/', views.delete_thought, name='delete_thought'),
    path('toggle-public-thoughts/', views.toggle_public_thoughts, name='toggle_public_thoughts'),
    
    # Authentication URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='thoughtify/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing_page'), name='logout'),
]
