from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import (
    REGEX, User, Review, Comment, Category, Genre, Title
)


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистранции нового пользователя."""

    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    username = serializers.RegexField(
        regex=REGEX,
        max_length=150,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Это имя уже занято'
            )
        if data['email'] == data['username']:
            raise serializers.ValidationError(
                'Поля не должны совпадать'
            )
        return data


class TokenObtainSerializer(serializers.ModelSerializer):
    """Сериализатор для получения токена."""

    username = serializers.RegexField(
        regex=REGEX,
        max_length=150,
        required=True,
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate_username(self, value):
        get_object_or_404(User, username=value)
        return value


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        exclude = ['id']
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        exclude = ['id']
        lookup_field = 'slug'


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор для POST-запросов произведений."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор для GET-запросов произведений."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        exclude = ['title']
        read_only_fields = ['pub_date']

    def validate(self, data):
        """Один отзыв на одно произведение."""
        if self.context['request'].method != 'POST':
            return data
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        review = Review.objects.filter(author=author, title=title_id)
        if review:
            raise serializers.ValidationError(
                'На каждое произведение можно опубликовать только один отзыв.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
