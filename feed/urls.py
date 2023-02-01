from . import views
from django.urls import path


urlpatterns = [
    path('create/', views.create_post, name='create'),
    path('',  views.Feed.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('<slug:slug>/edit/', views.edit_post, name='edit'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('dislike/<slug:slug>',
         views.PostDislike.as_view(), name='post_dislike'),
    path('delete/<slug:slug>', views.PostDeleteView.as_view(),
         name='post_delete'),
    path('comment/delete/<pk>', views.CommentDeleteView.as_view(),
         name='comment_delete'),

]
