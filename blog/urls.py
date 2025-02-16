from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Blog Home
    path('', views.post_list, name='post_list'),

    # 📝 Post CRUD
    path('post/add/', views.add_post, name='add_post'),
    path('post/edit/<slug:slug>/', views.edit_post, name='edit_post'),
    path('post/delete/<slug:slug>/', views.delete_post, name='delete_post'),
    
    # 🏷️ Post Detail & Category
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<int:pk>/', views.category_posts, name='category_posts'),
    path('category/add/', views.add_category, name='add_category'),

    # ❤️ Likes System
    path('post/<slug:slug>/like/', views.like_post, name='like_post'),

    # 💬 Comments System
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
]
