from django.db import models
from users_app.models import CustomUser

# region Chat model
class Chat(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name='chats')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")
    
    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"
        ordering = ["-date_added"]
        db_table = 'chat'
    
    def __str__(self):
        return f"Chat betwen: {self.participants.first()} and {self.participants.last()}"
# endregion

# region Message model
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages', verbose_name="Chat")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="Sender")
    content = models.TextField(max_length=1000, verbose_name="Content")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")
    is_deleted = models.BooleanField(default=False, verbose_name="Is Deleted")
    is_edited = models.BooleanField(default=False, verbose_name="Is Edited")
    
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Message"
        ordering = ["timestamp"]
        db_table = 'message'
    
    def __str__(self):
        return f"{self.sender.username}: {self.content}"
# endregion

