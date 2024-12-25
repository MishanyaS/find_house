from django.contrib import admin
from admin_panel_app.models import Content

# Register your models here.
class ContentAdmin(admin.ModelAdmin):
    model = Content
    list_display = ['contacts_page_h5', 'change_date']
    search_fields = ['change_date']
    list_filter = ['change_date']

admin.site.register(Content, ContentAdmin)