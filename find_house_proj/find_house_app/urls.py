from django.urls import path, include
from find_house_app import views

urlpatterns = [
    # Home URLs
    path('', views.HomeView.as_view(), name='home'),

    # Announcement URLs
    path('announcement/<int:pk>/', views.AnnouncementDetailView.as_view(), name='announcement_read'),
    path('announcement/create/', views.AnnouncementCreateView.as_view(), name='announcement_create'),
    path('announcement/update/<int:pk>/', views.AnnouncementUpdateView.as_view(), name='announcement_update'),
    path('announcement/delete/<int:pk>/', views.AnnouncementDeleteView.as_view(), name='announcement_delete'),
    path('add-to-favorites/', views.AddToFavoritesView.as_view(), name='add_to_favorites'),

    # Search URLs
    path('search/', views.SearchAnnouncementView.as_view(), name='search'),
    path('search-news/', views.SearchNewsView.as_view(), name='search_news'),

    # Help URLs
    path('help/', views.HelpView.as_view(), name='help'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),

    # News URLs
    path('news-list/', views.NewsList.as_view(), name='news_list'),
    path('news/<int:pk>/', views.NewsDetail.as_view(), name='news_read'),

    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories-list/', views.CategoriesListView.as_view(), name='categories_list'),

    # Category Announcements URL
    path('category-announcements/<slug:cats>/', views.CategoryAnnouncementsView.as_view(), name='category_announcements'),

    # Favorite URLs
    path('favorite/', views.FavoriteView.as_view(), name='favorite'),

    # Comment URLs
    path('announcement/comment-add/<int:pk>/', views.CommentAddView.as_view(), name='comment_add'),
    path('comment/edit/<int:pk>/', views.CommentEditView.as_view(), name='comment_edit'),
    path('comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment_delete'),
]