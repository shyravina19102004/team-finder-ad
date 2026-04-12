from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Skill, User


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "name", "surname", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "name", "surname")
    ordering = ("email",)
    filter_horizontal = ("skills", "groups", "user_permissions")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Персональные данные",
            {"fields": ("name", "surname", "avatar", "phone", "github_url", "about")},
        ),
        ("Навыки", {"fields": ("skills",)}),
        (
            "Права доступа",
            {"fields": ("is_active", "is_staff", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "surname",
                    "phone",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
