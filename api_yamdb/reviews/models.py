from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .validators import validate_year


REGEX = r'^[\w.@+-]+\Z'


class User(AbstractUser):
    """Модель кастомного юзера"""

    class RoleChoice(models.TextChoices):
        USER = 'user', _('User')
        MODERATOR = 'moderator', _('Moderator')
        ADMIN = 'admin', _('Admin')

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Пользователь',
        validators=[
            RegexValidator(
                regex=REGEX,
                message='Поле содержит'
                        ' недопустимые символы'
            )
        ]
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Почта'
    )
    role = models.CharField(
        max_length=9,
        choices=RoleChoice.choices,
        default=RoleChoice.USER,
        verbose_name='Роль'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='О себе'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='usrname_email_constraint'
            ),
        ]

    def __str__(self) -> str:
        return self.username

    @property
    def is_admin(self):
        return (
            self.role == self.RoleChoice.ADMIN
            or self.is_superuser
        )

    @property
    def is_user(self):
        return self.role == self.RoleChoice.USER

    @property
    def is_moderator(self):
        return self.role == self.RoleChoice.MODERATOR


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(
        max_length=200,
        verbose_name='Категория',
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Адрес'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(
        max_length=50,
        verbose_name='Жанр',
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Адрес'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        max_length=200,
        verbose_name='Названия',
        unique=True
    )
    year = models.PositiveIntegerField(
        validators=[validate_year],
        verbose_name='Год издания',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    description = models.CharField(
        max_length=200,
        verbose_name='Описание',
        blank=True,
    )
    genre = models.ManyToManyField(Genre)

    class Meta:
        ordering = ('name', 'year')
        verbose_name = 'Произведение'

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    """Модель отзывов."""

    SCORE_CHOICE = enumerate(range(1, 11), start=1)

    text = models.TextField(
        verbose_name='Отзыв',
        blank=True,
        null=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        choices=SCORE_CHOICE
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    """Модель комментария."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        max_length=300
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text
