from . import views
from django.urls import path


urlpatterns = [
    path('create/', views.create_post, name='create'),
    path('',  views.Feed.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('<slug:slug>/edit/', views.edit_post, name='edit'),
]
