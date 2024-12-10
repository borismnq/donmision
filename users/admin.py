# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashe format
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('username')
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "is_admin", "is_active"]
    list_filter = ["is_staff"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name"]}),
        ("Security", {"fields": ["is_staff"]}),
        # ("Permissions", {"fields": ["is_admin",  "is_active"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2", "first_name"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []
# class CustomUserAdmin(UserAdmin):
#     model = User
#     list_display = [
#         "username",
#         "email",
#         "status",
#     ]
#     search_fields = [
#         "username",
#         "email"
#     ]
#     fieldsets = (
#         *UserAdmin.fieldsets,  # original form fieldsets, expanded
#         (
#             'Status',  # group heading of your choice; set to None for a blank space instead of a header
#             {
#                 'fields': (
#                     'status',
#                 ),
#             },        
#         ),
#         (                      # new fieldset added on to the bottom
#             'Extra Fields',  # group heading of your choice; set to None for a blank space instead of a header
#             {
#                 'fields': (

#                     'level',
#                     'address',
#                     'age',
#                     'gender',
#                 ),
#             },        
#         )
        
#     )
#     add_fieldsets = (
#         *UserAdmin.fieldsets,
#         (None, {
#             'classes': ('wide',),
#             'fields': (
#                 'status',
#                 'level',
#                 'phone_number',
#                 'address',
#                 'age',
#                 'gender',
#             ),
#         }),
#     )
#     ordering = ('email',)


# admin.site.register(User, CustomUserAdmin)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)