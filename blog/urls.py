from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('category/<int:pk>/', views.category_posts, name='category_posts'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/add/', views.add_post, name='add_post'),
    path('post/edit/<slug:slug>/', views.edit_post, name='edit_post'),
    path('post/delete/<slug:slug>/', views.delete_post, name='delete_post'),
]
