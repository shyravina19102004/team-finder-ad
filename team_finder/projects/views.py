from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from team_finder.constants import PAGINATE_PER_PAGE
from team_finder.service import paginate

from .forms import ProjectForm
from .models import Project


@login_required
def edit_project(request, project_id: int):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id != request.user.pk:
        return HttpResponseForbidden(
            "Доступ запрещён. Только автор проекта может его редактировать."
        )
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect("projects:project_detail", project_id=project.pk)
    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": True},
    )


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect("projects:project_detail", project_id=project.pk)
    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": False},
    )


def project_detail(request, project_id: int):
    project = get_object_or_404(Project, pk=project_id)
    return render(
        request,
        "projects/project-details.html",
        {"project": project}
    )


def project_list(request):
    # Оптимизация: подгружаем автора и количество участников
    projects_qs = Project.objects.select_related("owner").annotate(
        participants_count=Count("participants")
    ).order_by("-created_at")
    pagination_context = paginate(request, projects_qs, per_page=PAGINATE_PER_PAGE)
    return render(
        request,
        "projects/project_list.html",
        {
            "projects": pagination_context["page_obj"].object_list,
            **pagination_context,
        },
    )


@login_required
@require_POST
def toggle_participate(request, project_id: int):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    if project.participants.filter(pk=user.pk).exists():
        project.participants.remove(user)
    else:
        project.participants.add(user)
    return JsonResponse({"status": "ok"})


@login_required
@require_POST
def complete_project(request, project_id: int):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id != request.user.pk:
        return JsonResponse(
            {"error": "Only project owner can complete it"},
            status=HTTPStatus.FORBIDDEN
        )
    if project.status != Project.STATUS_OPEN:
        return JsonResponse(
            {"error": "Project is already closed"},
            status=HTTPStatus.BAD_REQUEST
        )
    project.status = Project.STATUS_CLOSED
    project.save()
    return JsonResponse({"status": "ok", "project_status": "closed"})