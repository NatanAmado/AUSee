from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.forum_home, name='home'),
    path('topics/', views.topic_list, name='topic_list'),
    path('topics/create/', views.create_topic, name='create_topic'),
    path('topics/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('topics/<int:topic_id>/edit-description/', views.edit_topic_description, name='edit_topic_description'),
    path('topics/<int:topic_id>/report/', views.report_topic, name='report_topic'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/create/<int:topic_id>/', views.create_post, name='create_post_in_topic'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/vote/', views.vote_post, name='vote_post'),
    path('search/', views.search_forum, name='search'),
] 