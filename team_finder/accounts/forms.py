from django import forms
from django.contrib.auth.password_validation import validate_password

from team_finder.constants import USER_NAME_MAX_LENGTH, USER_SURNAME_MAX_LENGTH
from team_finder.service import (
    normalize_phone,
    normalize_phone_for_comparison,
    validate_github_url,
)
from team_finder.accounts.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=USER_NAME_MAX_LENGTH)
    surname = forms.CharField(
        label="Фамилия",
        max_length=USER_SURNAME_MAX_LENGTH
    )
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Текущий пароль", widget=forms.PasswordInput
    )
    new_password1 = forms.CharField(
        label="Новый пароль", widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label="Подтвердите новый пароль", widget=forms.PasswordInput
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_old_password(self):
        current_password = self.cleaned_data.get("old_password")
        if current_password and not self.user.check_password(current_password):
            raise forms.ValidationError("Неверный текущий пароль")
        return current_password

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get("new_password1")
        new_password_confirmation = self.cleaned_data.get("new_password2")
        if new_password and new_password_confirmation and new_password != new_password_confirmation:
            self.add_error("new_password2", "Пароли не совпадают")

    def clean_new_password1(self):
        new_password = self.cleaned_data.get("new_password1")
        if new_password:
            validate_password(new_password, self.user)
        return new_password

    def save(self):
        self.user.set_password(self.cleaned_data["new_password1"])
        self.user.save()


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "surname", "avatar", "about", "phone", "github_url"]
        labels = {
            "name": "Имя",
            "surname": "Фамилия",
            "avatar": "Аватар",
            "about": "О себе",
            "phone": "Телефон",
            "github_url": "GitHub",
        }
        widgets = {
            "about": forms.Textarea(attrs={"rows": 4}),
            "avatar": forms.FileInput(attrs={"accept": "image/*"}),
        }

    def clean_phone(self):
        value = self.cleaned_data.get("phone", "").strip()
        normalized = normalize_phone(value)

        exclude_pk = self.instance.pk if self.instance else None
        for user in User.objects.exclude(pk=exclude_pk):
            if normalize_phone_for_comparison(user.phone) == normalized:
                raise forms.ValidationError("Этот номер телефона уже занят")
        return normalized

    def clean_github_url(self):
        value = self.cleaned_data.get("github_url", "").strip()
        return validate_github_url(value)
