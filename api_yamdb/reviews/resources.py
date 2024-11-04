from import_export import resources
from reviews.models import User, Review, Category, Genre, Title, Comment


class UserResource(resources.ModelResource):
    """Ресурс для экспорта объектов модели User."""

    class Meta:
        model = User


class CategoryResource(resources.ModelResource):
    """Ресурс для экспорта объектов модели Category."""

    class Meta:
        model = Category


class GenreResource(resources.ModelResource):
    """Ресурс для экспорта объектов модели Genre."""

    class Meta:
        model = Genre


class TitleResource(resources.ModelResource):
    """Ресурс для экспорта объектов модели Title."""

    genres = resources.Field(attribute='genre__name')

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category', 'genres', 'description')


class GenreTitleResource(resources.ModelResource):
    """Ресурс для экспорта объектов связанной модели GenreTitle."""

    genre = resources.Field(column_name='genre', attribute='genre__name')
    title = resources.Field(column_name='title', attribute='title__name')

    class Meta:
        model = Title
        fields = ('genre', 'title')


class ReviewResource(resources.ModelResource):
    """Ресурс для экспорта объектов модели Review."""

    class Meta:
        model = Review


class CommentResource(resources.ModelResource):
    """Ресурс для экспорта объектов модели Comment."""

    class Meta:
        model = Comment
