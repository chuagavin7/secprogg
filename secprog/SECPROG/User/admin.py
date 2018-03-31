from django.contrib import admin

# Register your models here.
from User.models import Staff, User

admin.site.register(User)
admin.site.register(Staff)
