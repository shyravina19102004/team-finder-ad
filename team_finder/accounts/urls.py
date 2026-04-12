from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("change-password/", views.change_password_view, name="change_password"),
    path("edit-profile/", views.edit_profile_view, name="edit_profile"),
    path("list/", views.participants_list, name="participants_list"),
    path("skills/", views.skills_autocomplete, name="skills_autocomplete"),
    path("<int:user_id>/skills/add/", views.add_skill_to_user, name="add_skill_to_user"),
    path(
        "<int:user_id>/skills/<int:skill_id>/remove/",
        views.remove_skill_from_user,
        name="remove_skill_from_user",
    ),
    path("<int:pk>/", views.user_details, name="user_details"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
]
