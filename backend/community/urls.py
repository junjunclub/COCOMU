"""

"""

from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.article_create, name="create"),
    path("<int:article_id>/", views.article_detail, name="detail"),
    path("<int:article_id>/update/", views.article_update, name="update"),
    path("<int:article_id>/delete/", views.article_delete, name="delete"),
    path(
        "<int:article_id>/comment_create/", views.comment_create, name="comment_create"
    ),
    path(
        "<int:article_id>/<int:comment_id>/comment_update/",
        views.comment_update,
        name="comment_update",
    ),
    path(
        "<int:article_id>/<int:comment_id>/comment_delete/",
        views.comment_delete,
        name="comment_delete",
    ),
    path("search/<str:keyword>", views.search, name="search",),
]
