from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


from .models import Profile, Review

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class ReviewInLine(admin.StackedInline):
    model = Review
    can_delete = False
    verbose_name_plural = 'Reviews'
    fk_name = 'reviewed'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, ReviewInLine )

    list_display = ('username','email','first_name','last_name','get_company','is_active')
    list_editable = ('is_active',)

    def get_company(self, obj):
        return obj.profile.company
    get_company.admin_order_field  = 'company'
    get_company.short_description = 'Company'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)




admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

