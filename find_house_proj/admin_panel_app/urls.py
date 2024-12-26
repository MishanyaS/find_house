from django.urls import path
from admin_panel_app import views

app_name = 'admin_panel_app'

urlpatterns = [
    # Admin Home URLs
    path('', views.AdminPanelHomeView.as_view(), name='admin_index'),
    
    # Admin Users URLs
    path('users-list/', views.UserListView.as_view(), name='admin_user_list_index'),
    path('users-details/<int:pk>/', views.UserDetailView.as_view(), name='admin_user_read'),
    path('user/delete/<int:pk>/', views.UserDeleteView.as_view(), name='admin_user_delete'),
    path('user/add/', views.UserCreateView.as_view(), name='admin_user_create'),
    path('user/edit/<int:pk>/', views.UserUpdateView.as_view(), name='admin_user_update'),
    
    # Admin Announcements URLs
    path('announcements-list/', views.AnnouncementListView.as_view(), name='admin_announcement_list'),
    path('announcements-details/<int:pk>/', views.AnnouncementDetailView.as_view(), name='admin_announcement_read'),
    path('announcement/delete/<int:pk>/', views.AnnouncementDeleteView.as_view(), name='admin_announcement_delete'),
    path('announcement/add/', views.AnnouncementCreateView.as_view(), name='admin_announcement_create'),
    path('announcement/edit/<int:pk>/', views.AnnouncementUpdateView.as_view(), name='admin_announcement_update'),
    
    # Admin Announcement Images URLs
    path('announcement-images-list/', views.AnnouncementImageListView.as_view(), name='admin_announcement_images_list'),
    path('announcement-images-details/<int:pk>/', views.AnnouncementImageDetailView.as_view(), name='admin_announcement_images_read'),
    path('announcement-images/delete/<int:pk>/', views.AnnouncementImageDeleteView.as_view(), name='admin_announcement_images_delete'),
    path('announcement-images/add/', views.AnnouncementImageCreateView.as_view(), name='admin_announcement_images_create'),
    path('announcement-images/edit/<int:pk>/', views.AnnouncementImageUpdateView.as_view(), name='admin_announcement_images_update'),
    
    # Admin Categories URLs
    path('categories-list/', views.CategoryListView.as_view(), name='admin_categories_list'),
    path('categories-details/<int:pk>/', views.CategoryDetailView.as_view(), name='admin_category_read'),
    path('category/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='admin_category_delete'),
    path('category/add/', views.CategoryCreateView.as_view(), name='admin_category_create'),
    path('category/edit/<int:pk>/', views.CategoryUpdateView.as_view(), name='admin_category_update'),
    
    # Admin Favorites URLs
    path('favorites-list/', views.FavoriteListView.as_view(), name='admin_favorites_list'),
    path('favorites-details/<int:pk>/', views.FavoriteDetailView.as_view(), name='admin_favorite_read'),
    path('favorite/delete/<int:pk>/', views.FavoriteDeleteView.as_view(), name='admin_favorite_delete'),
    path('favorite/add/', views.FavoriteCreateView.as_view(), name='admin_favorite_create'),
    path('favorite/edit/<int:pk>/', views.FavoriteUpdateView.as_view(), name='admin_favorite_update'),
    
    # Admin News URLs
    path('news-list/', views.NewsListView.as_view(), name='admin_news_list'),
    path('news-details/<int:pk>/', views.NewsDetailView.as_view(), name='admin_news_read'),
    path('news/delete/<int:pk>/', views.NewsDeleteView.as_view(), name='admin_news_delete'),
    path('news/add/', views.NewsCreateView.as_view(), name='admin_news_create'),
    path('news/edit/<int:pk>/', views.NewsUpdateView.as_view(), name='admin_news_update'),
    
    # Admin Announcement View Histories URLs
    path('announcement-view-histories-list/', views.AnnouncementViewHistoryListView.as_view(), name='admin_announcement_view_histories_list'),
    path('announcement-view-histories-details/<int:pk>/', views.AnnouncementViewHistoryDetailView.as_view(), name='admin_announcement_view_history_read'),
    path('announcement-view-history/delete/<int:pk>/', views.AnnouncementViewHistoryDeleteView.as_view(), name='admin_announcement_view_history_delete'),
    path('announcement-view-history/add/', views.AnnouncementViewHistoryCreateView.as_view(), name='admin_announcement_view_history_create'),
    path('announcement-view-history/edit/<int:pk>/', views.AnnouncementViewHistoryUpdateView.as_view(), name='admin_announcement_view_history_update'),
    
    # Admin Comments URLs
    path('comments-list/', views.CommentListView.as_view(), name='admin_comments_list'),
    path('comments-details/<int:pk>/', views.CommentDetailView.as_view(), name='admin_comment_read'),
    path('comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), name='admin_comment_delete'),
    path('comment/add/', views.CommentCreateView.as_view(), name='admin_comment_create'),
    path('comment/edit/<int:pk>/', views.CommentUpdateView.as_view(), name='admin_comment_update'),
    
    # Admin Chats URLs
    path('chats-list/', views.ChatListView.as_view(), name='admin_chats_list'),
    path('chats-details/<int:pk>/', views.ChatDetailView.as_view(), name='admin_chat_read'),
    path('chat/delete/<int:pk>/', views.ChatDeleteView.as_view(), name='admin_chat_delete'),
    path('chat/add/', views.ChatCreateView.as_view(), name='admin_chat_create'),
    path('chat/edit/<int:pk>/', views.ChatUpdateView.as_view(), name='admin_chat_update'),
    
    # Admin Messages URLs
    path('messages-list/', views.MessageListView.as_view(), name='admin_messages_list'),
    path('messages-details/<int:pk>/', views.MessageDetailView.as_view(), name='admin_message_read'),
    path('message/delete/<int:pk>/', views.MessageDeleteView.as_view(), name='admin_message_delete'),
    path('message/add/', views.MessageCreateView.as_view(), name='admin_message_create'),
    path('message/edit/<int:pk>/', views.MessageUpdateView.as_view(), name='admin_message_update'),

    # Admin Content URLs
    path('content-list/', views.ContentListView.as_view(), name='admin_content_list'),
    path('content-details/<int:pk>/', views.ContentDetailView.as_view(), name='admin_content_read'),
    path('content/delete/<int:pk>/', views.ContentDeleteView.as_view(), name='admin_content_delete'),
    path('content/add/', views.ContentCreateView.as_view(), name='admin_content_create'),
    path('content/edit/<int:pk>/', views.ContentUpdateView.as_view(), name='admin_content_update'),
]

