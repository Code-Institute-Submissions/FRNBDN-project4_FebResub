from . import views
from django.urls import path


urlpatterns = [
    path('',  views.Feed.as_view(), name='home'),
    path('create/', views.CreatePost.as_view(), name='create'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]
