from django.contrib import admin
from authentication.models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email']


admin.site.register(User, UserAdmin)
