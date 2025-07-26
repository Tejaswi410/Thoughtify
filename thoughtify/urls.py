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
    path('thought/<int:thought_id>/like/', views.like_thought, name='like_thought'),
    
    # Authentication URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing_page'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('my-thoughts/', views.my_thoughts_view, name='my_thoughts'),
]
