from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "participants_count", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "description")
    filter_horizontal = ("participants",)
    readonly_fields = ("created_at",)
    list_editable = ("status",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(participants_count=Count("participants"))

    @admin.display(description="Участников", ordering="participants_count")
    def participants_count(self, obj):
        return obj.participants_count
