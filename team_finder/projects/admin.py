from django.contrib import admin
from django.db.models import Count

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "participants_count", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "description")
    filter_horizontal = ("participants",)
    readonly_fields = ("created_at",)
    list_editable = ("status",)  # возможность менять статус прямо в списке

    def participants_count(self, obj):
        return obj.participants_count
    participants_count.short_description = "Участников"
    participants_count.admin_order_field = "participants_count"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Аннотируем количество участников для оптимизации
        return queryset.annotate(participants_count=Count("participants"))