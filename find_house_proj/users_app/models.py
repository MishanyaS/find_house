from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from datetime import date
from dateutil.relativedelta import relativedelta


# Create your models here.
# region  CustomUser model
class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group,related_name='customuser_groups',blank=True)
    user_permissions = models.ManyToManyField(Permission,related_name='customuser_permissions',blank=True)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '999999999'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], unique=True, max_length=17, blank=True, null=True, help_text="Enter phone number in the format: '999999999'. Up to 10 digits allowed.", verbose_name="Phone Number")
    birth_date = models.DateField(null=True, blank=True, validators=[MinValueValidator(date(1900, 1, 1)), MaxValueValidator(date.today() - relativedelta(years=18))], verbose_name="Date of Birth")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address")  
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='', verbose_name="User Avatar")  
    description = models.TextField(max_length=1000, blank=True, null=True, verbose_name="Profile Description")
    is_admin = models.BooleanField(default=False, verbose_name="Is Admin")
    
    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        ordering = ["-date_joined"]
        db_table = 'custom_user'
    
    def __str__(self):
        return f"{self.username}"
# endregion
