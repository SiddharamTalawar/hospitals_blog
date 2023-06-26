from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('', HomeView.as_view() , name='home' ),
    path('add_post/',add_postview.as_view(), name='add_post'),
    path('artical/<int:pk>',artical_detailview.as_view(),name='detail_view'),
    path('delete/<int:pk>',delete_post_view.as_view(),name='delete_post'),
    path('artical/edit/<int:pk>',upadte_post_view.as_view(),name='update_post'),
    path('categorylist/<str:cat>',categoryview,name='category_sort'),
    path('create_profile',Create_ProfilePage_View.as_view(),name='create_profile'),
    path('user_profile/<int:pk>',Show_ProfilePage_View.as_view(),name='user_profile'),
    path('edit_profile/<int:pk>',upadte_profile_view.as_view(),name='edit_profile'),
    path('my_post/',my_post_view,name='my_posts'),
    
    

]    