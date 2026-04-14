from django import forms

from team_finder.service import validate_github_repo_url

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
        url = self.cleaned_data.get("github_url", "").strip()
        return validate_github_repo_url(url)
