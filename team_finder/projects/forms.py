from urllib.parse import urlparse

from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]
        labels = {
            "name": "Название",
            "description": "Описание",
            "github_url": "Ссылка на GitHub",
            "status": "Статус",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_github_url(self):
        url = self.cleaned_data.get("github_url")
        if not url:
            return url

        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https") or parsed.netloc not in (
            "github.com",
            "www.github.com",
        ):
            raise forms.ValidationError(
                "Введите корректную ссылку на репозиторий GitHub "
                "(например, https://github.com/user/repo)."
            )

        path_parts = [p for p in parsed.path.split("/") if p]
        if len(path_parts) < 2:
            raise forms.ValidationError(
                "Ссылка должна указывать на конкретный репозиторий GitHub "
                "(формат: https://github.com/user/repo)."
            )

        return url
