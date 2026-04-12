<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path("", lambda request: redirect('projects:project_list')),
    path("admin/", admin.site.urls),
    path("projects/", include("team_finder.projects.urls")),
    path("users/", include("team_finder.accounts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

]
>>>>>>> 4e5422aae3382a86db5ad8c67f60db6d95aab449
