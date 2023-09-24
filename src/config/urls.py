from django.contrib import admin
from django.urls import include, path
from lists import urls as list_urls
from lists import views as list_views

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("", list_views.home_page, name="home"),
    path("lists/", include(list_urls)),
]
