from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

# Create your models here.
# region  Content model
class Content(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '999999999'. Up to 10 digits allowed.")
    contacts_page_h5 = models.TextField(max_length=255, verbose_name="Contacts Page h5")
    contacts_page_text = models.TextField(max_length=10000, verbose_name="Contacts Page Text")
    contacts_page_address = models.TextField(max_length=255, verbose_name="Contacts Page Address")
    contacts_page_telephone = models.TextField(max_length=255, validators=[phone_regex], blank=False, null=False, verbose_name="Contacts Page Telephone")
    contacts_page_email = models.EmailField(max_length=255, verbose_name="Contacts Page Email")
    footer_text = models.TextField(max_length=10000, verbose_name="Footer Text")
    change_date = models.DateTimeField(auto_now_add=True, verbose_name="Change Date")

    class Meta:
        verbose_name = "Content"
        verbose_name_plural = "Content"
        ordering = ["change_date"]
        db_table = 'content'
    
    def __str__(self):
        return "Content"
# endregion
