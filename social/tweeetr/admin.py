from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Tweeet

# Register your models here.
# UNREGISTER GROUPS
admin.site.unregister(Group)


class ProfileInLine(admin.StackedInline):
    model = Profile


# EXTEND USER MODEL
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInLine]


# unregister user
admin.site.unregister(User)
# reregister user
admin.site.register(User, UserAdmin)
#admin.site.register(Profile)
admin.site.register(Tweeet)


