from django.db import models
from django.urls import reverse
from users_app.models import CustomUser
from slugify import slugify

# Create your models here.
# region Category model
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Category Name")
    description = models.TextField(max_length=1000, blank=True, verbose_name="Description")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]
        db_table = 'category'

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("find_house_app:category_announcements", args=[str(self.name)])
# endregion

# region Announcement model
class Announcement(models.Model):
    ACTIVE = 1
    SOLD = 2
    WITHDRAWN = 3
    ANNOUNCEMENT_STATUSES = ((ACTIVE, 'ACTIVE'), (SOLD, 'SOLD'), (WITHDRAWN, 'WITHDRAWN'),)

    title = models.CharField(max_length=255, unique=True, verbose_name="Title")
    description = models.TextField(max_length=5000, blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    square = models.IntegerField(verbose_name="Square")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Owner")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="announcements", verbose_name="Category")
    status = models.SmallIntegerField(choices=ANNOUNCEMENT_STATUSES, verbose_name="Status")
    address = models.CharField(max_length=255, unique=True, verbose_name="Address")
    views = models.IntegerField(default=0, verbose_name="Views")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")
    slug = models.SlugField(max_length=255, unique=True, null=False, blank=False, default='', editable=False)

    class Meta:
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"
        ordering = ["-date_added"]
        db_table = 'announcement'

    def __str__(self):
        return f"Title: {self.title} Owner: {self.owner} Category: {self.category} Status: {self.status}"

    def get_absolute_url(self):
        return reverse('announcement_detail', args=[str(self.pk)])
    
    def price_per_square(self):
        if self.square == 0:
            return 0
        return self.price/self.square
# endregion

# region AnnouncementImage model
class AnnouncementImage(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='images', verbose_name="Announcement")
    image = models.ImageField(upload_to='announcements/', height_field='image_height', width_field='image_width', verbose_name="Image")
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, verbose_name="Image Height")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, verbose_name="Image Width")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Description")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")

    class Meta:
        verbose_name = "Announcement Image"
        verbose_name_plural = "Announcement Images"
        ordering = ["-date_added"]
        db_table = 'announcement_image'

    def __str__(self):
        return f"Image ID: {self.id} for {self.announcement.title}"
    
    def get_absolute_url(self):
        return reverse('details_announcement_image')
    
    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super().delete(*args, **kwargs)
# endregion

# region Comment model
class Comment(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comments', verbose_name="Announcement")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="User")
    text = models.TextField(max_length=1000, verbose_name="Comment Text")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-date_added"]
        db_table = 'comment'

    def __str__(self):
        return f"{self.user.username} - {self.date_added}"
# endregion

# region News model
class News(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Title")
    content = models.TextField(blank=False, null=False, max_length=5000, verbose_name="Content")
    views_count = models.IntegerField(default=0, verbose_name="Views Count")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")
    slug = models.SlugField(max_length=255, unique=True, null=False, blank=False, default='', editable=False)
    
    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News List"
        ordering = ["-date_added"]
        db_table = 'news'
        
    def __str__(self):
        return f"News Title: {self.title} Date: {self.content}"
    
    def get_absolute_url(self):
        return reverse('details_news')
# endregion

# region AnnouncementViewHistory model
class AnnouncementViewHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name="User")
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, verbose_name="Announcement")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")

    class Meta:
        verbose_name = "Announcement View History"
        verbose_name_plural = "Announcement View Histories"
        ordering = ["-date"]
        db_table = 'announcement_view_history'

    def __str__(self):
        return f"{self.user} viewed announcement \"{self.announcement}\" on {self.date}"
# endregion

# region Favorite model
class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="favorites", verbose_name="User")
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="favorited_by", verbose_name="Announcement")
    is_in_favorite = models.BooleanField(default=False, verbose_name="Is in Favorite")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")

    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"
        unique_together = [("user", "announcement")]
        ordering = ["-date_added"]
        db_table = 'favorite'

    def __str__(self):
        return f"{self.user} favorited {self.announcement} on {self.date_added}"
# endregion

