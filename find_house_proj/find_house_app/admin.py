from django.contrib import admin
from find_house_app.models import Category, Announcement, AnnouncementImage, Comment, News, AnnouncementViewHistory, Favorite

# Register your models here.
# region AnnouncementImage admin
class AnnouncementImageInline(admin.TabularInline):
    model = AnnouncementImage
    extra = 3

class AnnouncementImageAdmin(admin.ModelAdmin):
    model = AnnouncementImage
    list_display = ['announcement', 'image']
    search_fields = ['announcement__title', 'announcement__price']
    list_filter = ['announcement__title', 'announcement__price']
# endregion

# region Category admin
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name', 'description', 'date_added']
    search_fields = ['name', 'description']
    list_filter = ['name', 'description']
# endregion

# region Announcement admin
class AnnouncementAdmin(admin.ModelAdmin):
    model = Announcement
    list_display = ['title', 'price', 'date_added']
    search_fields = ['title', 'price']
    list_filter = ['title', 'price']
# endregion

# region Comment admin
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['get_announcement_title', 'get_user_username', 'text', 'date_added']
    search_fields = ['get_announcement_title', 'text']
    list_filter = ['id', 'text']

    def get_user_username(self, obj):
        return obj.user.username
    get_user_username.short_description = 'Username'

    def get_announcement_title(self, obj):
        return obj.announcement.title
    get_announcement_title.short_description = 'Announcement Title'
# endregion

# region News admin
class NewsAdmin(admin.ModelAdmin):
    model = News
    list_display = ['title', 'content', 'views_count', 'date_added']
    search_fields = ['title', 'content']
    list_filter = ['title', 'content']
# endregion

# region AnnouncementViewHistory admin
class AnnouncementViewHistoryAdmin(admin.ModelAdmin):
    model = AnnouncementViewHistory
    list_display = ['get_user_username', 'get_announcement_title', 'date']
    search_fields = ['get_user_username', 'get_announcement_title']
    list_filter = ['id',]

    def get_user_username(self, obj):
        return obj.user.username
    get_user_username.short_description = 'Username'

    def get_announcement_title(self, obj):
        return obj.announcement.title
    get_announcement_title.short_description = 'Announcement Title'
# endregion

# region Favorite admin
class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = ['get_user_username', 'get_announcement_title', 'is_in_favorite', 'date_added']
    search_fields = ['get_user_username', 'get_announcement_title']
    list_filter = ['id',]

    def get_user_username(self, obj):
        return obj.user.username
    get_user_username.short_description = 'Username'

    def get_announcement_title(self, obj):
        return obj.announcement.title
    get_announcement_title.short_description = 'Announcement Title'
# endregion

admin.site.register(AnnouncementImage, AnnouncementImageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(AnnouncementViewHistory, AnnouncementViewHistoryAdmin)
admin.site.register(Favorite, FavoriteAdmin)

