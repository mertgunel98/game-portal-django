from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/<slug:slug>/', views.game_detail, name='game_detail'),
    path('browse/', views.browse, name='browse'),
    path('wishlist/', views.watchlist_view, name='wishlist'),
    path('wishlist/toggle/<int:game_id>/', views.toggle_watchlist, name='toggle_watchlist'),
    path('game/<int:game_id>/review/', views.add_review, name='add_review'),
    path('signup/', views.auth_signup, name='signup'),
    path('login/', views.auth_login, name='login'),
    path('logout/', views.auth_logout, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/game/add/', views.add_game, name='add_game'),
    path('admin-dashboard/game/delete/<int:game_id>/', views.delete_game, name='delete_game'),
    path('admin-dashboard/game/toggle-featured/<int:game_id>/', views.toggle_featured, name='toggle_featured'),
    path('admin-dashboard/review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    
    # REST API endpoints
    path('api/games/', views.api_game_list, name='api_game_list'),
    path('api/games/<int:game_id>/', views.api_game_detail, name='api_game_detail'),
]
