from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import User, Review, Category, Genre, Title, Comment
from .import_export import (
    UserResource, CategoryResource, GenreResource,
    TitleResource, ReviewResource, CommentResource,
    GenreTitleResource
)


@admin.register(User)
class UserAdmin(ImportExportMixin, admin.ModelAdmin):
    """Админка для модели User, с возможностью экспорта/импорта."""

    resource_class = UserResource


@admin.register(Category)
class CategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    """Админка для модели Category, с возможностью экспорта/импорта."""

    resource_class = CategoryResource


@admin.register(Genre)
class GenreAdmin(ImportExportMixin, admin.ModelAdmin):
    """Админка для модели Genre, с возможностью экспорта/импорта."""

    resource_class = GenreResource


@admin.register(Title)
class TitleAdmin(ImportExportMixin, admin.ModelAdmin):
    """Админка для модели Title, с возможностью экспорта/импорта."""

    resource_class = TitleResource


class GenreTitleAdmin(ImportExportMixin, admin.ModelAdmin):
    """Админка для связной модели GenreTitle, с экспортом/импортом."""

    list_display = ('genre', 'title')
    resource_class = GenreTitleResource


admin.site.register(Title.genre.through, GenreTitleAdmin)


@admin.register(Review)
class ReviewAdmin(ImportExportMixin, admin.ModelAdmin):
    """Админка для модели Review, с возможностью экспорта/импорта."""

    resource_class = ReviewResource


@admin.register(Comment)
class CommentAdmin(ImportExportMixin, admin.ModelAdmin):
    """Админка для модели Comment, с возможностью экспорта/импорта."""

    resource_class = CommentResource
