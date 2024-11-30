from django.contrib import admin
from chat_app.models import Chat, Message

# Register your models here.
# region Chat admin
class ChatAdmin(admin.ModelAdmin):
    model = Chat
    list_display = ['date_added']
    search_fields = ['date_added']
    list_filter = ['date_added']
# endregion

# region Message admin
class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ['chat', 'sender', 'content', 'timestamp']
    search_fields = ['sender']
    list_filter = ['timestamp']
# endregion

# Models registration
admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
