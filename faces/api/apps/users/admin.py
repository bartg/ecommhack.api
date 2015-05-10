from ckeditor_demo.demo_application import forms
from django.contrib import admin

# Register your models here.
from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.forms.models import ModelForm
from django.forms.widgets import PasswordInput
from faces.api.apps.users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'created_at')

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal', {'fields': ('username', 'name')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = fieldsets
    search_fields = ('email', 'name', 'username')
    ordering = ('email', '-created_at',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)