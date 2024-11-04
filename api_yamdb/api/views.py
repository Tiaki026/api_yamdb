import csv
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters, viewsets, pagination
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.db.models import Avg

from reviews.filters import TitleFilter
from reviews.models import User, Review, Category, Genre, Title
from .permissions import (
    IsAdminIsSuperuser, IsAuthorOrSuperUserOrReadOnly, IsAdminOrAllowGet
)
from .serializers import (
    SignUpSerializer, TokenObtainSerializer, UserSerializer, ReviewSerializer,
    CommentSerializer, CategorySerializer, GenreSerializer,
    TitleGetSerializer, TitlePostSerializer,
)
from .mixins import CustomViewSetMixin
from .utils import send_confirmation_code


class SignupViewSet(CreateAPIView):
    """Регистрация с подтвердением по email."""

    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(**serializer.validated_data)
            confirmation_code = default_token_generator.make_token(user)
            send_confirmation_code(user.email, confirmation_code)
            return Response(serializer.data, status=200)
        except IntegrityError:
            return Response(
                'username или email уже заняты',
                status=400
            )


class TokenObtainViewSet(CreateAPIView):
    """Представление для получения JWT токена."""

    serializer_class = TokenObtainSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.validated_data
        user = get_object_or_404(
            User, username=valid_data['username']
        )
        if not default_token_generator.check_token(
            user,
            valid_data['confirmation_code']
        ):
            return Response(
                {'error': 'Incorrect confirmation_code'},
                status=400
            )
        token = AccessToken.for_user(user)
        return Response(str(token), status=200)


class UserViewSet(viewsets.ModelViewSet):
    """Представление для управления информацией пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAdminIsSuperuser,)
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^username',)

    @action(
        detail=False,
        methods=('get', 'patch'),
        permission_classes=(permissions.IsAuthenticated,),
        url_path='me',
        url_name='me',
    )
    def get_me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=200)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=200)


class CategoryViewSet(CustomViewSetMixin):
    """Представление для вывода списка категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrAllowGet]


class GenreViewSet(CustomViewSetMixin):
    """Представление для вывода списка жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrAllowGet]


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для вывода списка произведений."""

    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('id')
    serializer_class = TitleFilter
    permission_classes = [IsAdminOrAllowGet]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitlePostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для вывода списка отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrSuperUserOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для вывода списка комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrSuperUserOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


def import_csv(request):
    """Импортирование csv-файлов в базу."""
    if request.method == 'POST':
        file = request.FILES['csv_file']
        reader = csv.DictReader(file.read().decode('utf-8').splitlines())
        for row in reader:
            genre, _ = Genre.objects.get_or_create(
                slug=row['genre_slug'],
                defaults={'name': row['genre_name']}
            )
            category, _ = Category.objects.get_or_create(
                slug=row['category_slug'],
                defaults={'name': row['category_name']}
            )
            title, _ = Title.objects.get_or_create(
                name=row['title_name'],
                defaults={
                    'slug': row['title_slug'],
                    'genre': genre,
                    'category': category,
                }
            )
        return render(request, 'import_csv.html', {'success': True})
    return render(request, 'import_csv.html')
