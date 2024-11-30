from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users_app.models import CustomUser

# Register your models here.
# region CustomUser admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'phone_number', 'birth_date', 'email', 'is_active', 'is_staff', 'is_admin']
    search_fields = ['username', 'phone_number', 'email']
    list_filter = ['username', 'phone_number', 'email']
# endregion

admin.site.register(CustomUser, CustomUserAdmin)
