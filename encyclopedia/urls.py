from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search_view, name="search_view"),
    path("newentry/", views.newentry_view, name="newentry_view"),
    path("editentry/<str:key>/", views.editentry_view, name="editentry_view"),
    path("update/<str:key>/", views.updatentry, name="updatentry"),
    path("random/", views.randomentry, name="randomentry"),
    path("<str:key>/", views.entry, name="entry")
]

