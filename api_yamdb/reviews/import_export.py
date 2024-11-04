from import_export import resources
from reviews.models import User, Review, Category, Genre, Title, Comment


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre


class TitleResource(resources.ModelResource):
    genres = resources.Field(attribute='genre__name')

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category', 'genres', 'description')


class GenreTitleResource(resources.ModelResource):
    genre = resources.Field(column_name='genre', attribute='genre__name')
    title = resources.Field(column_name='title', attribute='title__name')

    class Meta:
        model = Title
        fields = ('genre', 'title')


class ReviewResource(resources.ModelResource):
    class Meta:
        model = Review


class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment
