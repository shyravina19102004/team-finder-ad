import json
from http import HTTPStatus

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from team_finder.constants import PAGINATE_PER_PAGE, SKILLS_AUTOCOMPLETE_LIMIT
from team_finder.service import paginate
from team_finder.accounts.forms import ChangePasswordForm, EditProfileForm, LoginForm, RegisterForm
from team_finder.accounts.models import Skill, User


def user_details(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, "users/user-details.html", {"user": user})


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = User.objects.create_user(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
            name=form.cleaned_data["name"],
            surname=form.cleaned_data["surname"],
            phone="",
        )
        login(request, user)
        return redirect("projects:project_list")
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )
        if user is not None:
            login(request, user)
            return redirect("projects:project_list")
        form.add_error(None, "Неверный имейл или пароль")
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("projects:project_list")


@login_required
def change_password_view(request):
    form = ChangePasswordForm(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("users:user_details", pk=request.user.pk)
    return render(request, "users/change_password.html", {"form": form})


@login_required
def edit_profile_view(request):
    form = EditProfileForm(
        request.POST or None, request.FILES or None, instance=request.user
    )
    if form.is_valid():
        form.save()
        return redirect("users:user_details", pk=request.user.pk)
    return render(request, "users/edit_profile.html", {"form": form})


def participants_list(request):
    participants_qs = User.objects.all()
    active_skill = None

    skill_id = request.GET.get("skill")
    if skill_id:
        participants_qs = participants_qs.filter(skills__id=skill_id)
        try:
            active_skill = Skill.objects.get(pk=skill_id)
        except Skill.DoesNotExist:
            pass

    pagination_context = paginate(
        request,
        participants_qs,
        per_page=PAGINATE_PER_PAGE
    )

    return render(
        request,
        "users/participants.html",
        {
            "participants": pagination_context["page_obj"].object_list,
            **pagination_context,
            "all_skills": Skill.objects.all().order_by("name"),
            "active_skill": active_skill,
        },
    )


def skills_autocomplete(request):
    if request.method != "GET":
        return JsonResponse([], safe=False)

    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse([], safe=False)

    skills = list(
        Skill.objects.filter(name__istartswith=query)
        .order_by("name")
        .values("id", "name")[:SKILLS_AUTOCOMPLETE_LIMIT]
    )
    return JsonResponse(skills, safe=False)


@require_POST
def add_skill_to_user(request, user_id: int):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "Forbidden"},
            status=HTTPStatus.FORBIDDEN,
        )

    user = get_object_or_404(User, pk=user_id)

    if user.pk != request.user.pk:
        return JsonResponse(
            {"error": "Forbidden"},
            status=HTTPStatus.FORBIDDEN,
        )

    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=HTTPStatus.BAD_REQUEST,
        )

    has_skill_id = "skill_id" in data
    has_name = "name" in data

    if has_skill_id and has_name:
        return JsonResponse(
            {"error": "Provide only skill_id or name"},
            status=HTTPStatus.BAD_REQUEST,
        )
    if not has_skill_id and not has_name:
        return JsonResponse(
            {"error": "Provide skill_id or name"},
            status=HTTPStatus.BAD_REQUEST,
        )

    created = False
    added = False

    if has_skill_id:
        try:
            skill = Skill.objects.get(pk=data["skill_id"])
        except (Skill.DoesNotExist, TypeError, ValueError):
            return JsonResponse(
                {"error": "Skill not found"},
                status=HTTPStatus.NOT_FOUND,
            )
        if user.skills.filter(pk=skill.pk).exists():
            return JsonResponse(
                {"skill_id": skill.pk, "created": False, "added": False},
                status=HTTPStatus.OK,
            )
        user.skills.add(skill)
        added = True
    else:
        name = data.get("name")
        if name is None or not isinstance(name, str):
            return JsonResponse(
                {"error": "name must be a non-empty string"},
                status=HTTPStatus.BAD_REQUEST,
            )
        name = name.strip()
        if not name:
            return JsonResponse(
                {"error": "name must be a non-empty string"},
                status=HTTPStatus.BAD_REQUEST,
            )

        skill = Skill.objects.filter(name__iexact=name).first()
        if skill is None:
            skill = Skill.objects.create(name=name)
            created = True
        if user.skills.filter(pk=skill.pk).exists():
            return JsonResponse(
                {
                    "skill_id": skill.pk,
                    "created": created,
                    "added": False,
                },
                status=HTTPStatus.OK,
            )
        user.skills.add(skill)
        added = True

    return JsonResponse(
        {"skill_id": skill.pk, "created": created, "added": added},
        status=HTTPStatus.OK,
    )


@require_POST
def remove_skill_from_user(request, user_id: int, skill_id: int):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "Forbidden"},
            status=HTTPStatus.FORBIDDEN,
        )

    user = get_object_or_404(User, pk=user_id)

    if user.pk != request.user.pk:
        return JsonResponse(
            {"error": "Forbidden"},
            status=HTTPStatus.FORBIDDEN,
        )

    try:
        skill = Skill.objects.get(pk=skill_id)
    except (Skill.DoesNotExist, ValueError, TypeError):
        return JsonResponse(
            {"error": "Skill not found"},
            status=HTTPStatus.NOT_FOUND,
        )

    if not user.skills.filter(pk=skill.pk).exists():
        return JsonResponse(
            {"error": "User does not have this skill"},
            status=HTTPStatus.NOT_FOUND,
        )

    user.skills.remove(skill)
    return JsonResponse(
        {"status": "ok"},
        status=HTTPStatus.OK,
    )
